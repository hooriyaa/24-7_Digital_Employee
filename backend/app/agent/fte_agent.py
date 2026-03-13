"""
FTEAgent - Customer Success Digital FTE AI Agent.

Base agent class with skills for customer support automation.
"""
import asyncio
import json
import re
from typing import Any, Optional

from pydantic import BaseModel

# Import OpenAI Agents SDK with fallback for different package versions
try:
    from openai_agents import Agent, Runner, function_tool, RunConfig
except ImportError:
    from agents import Agent, Runner, function_tool, RunConfig

from app.config import get_settings
from app.crud import customer_crud, ticket_crud, message_crud
from app.agent.skills.knowledge_retrieval import knowledge_retrieval_skill
from app.agent.skills.search_knowledge_base import search_knowledge_base
from app.agent.skills.context7_docs import external_docs_search, multi_library_search
from app.agent.skills.human_escalation import human_escalation
from app.agent.providers import provider_manager
from app.services.nlp import sentiment_service
from app.services.tool_selector import tool_selector, ToolType


class FTEAgentConfig(BaseModel):
    """Configuration for FTEAgent."""
    model: str = "litellm/gemini/gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 2000
    enable_knowledge_retrieval: bool = True
    enable_sentiment_analysis: bool = True
    escalation_threshold: float = 0.7


class FTEAgent:
    """
    Customer Success Digital FTE Agent.

    An AI agent specialized in customer support with the following capabilities:
    - Knowledge retrieval from knowledge base (pgvector)
    - Customer lookup and management
    - Ticket creation and management
    - Message handling
    - Sentiment analysis
    - Escalation detection

    The agent uses the OpenAI Agents SDK with custom function tools.
    """

    def __init__(self, config: Optional[FTEAgentConfig] = None):
        """
        Initialize FTE Agent.

        Args:
            config: Optional agent configuration
        """
        self.config = config or FTEAgentConfig()
        self.settings = get_settings()
        self._agent: Optional[Agent] = None

    def _create_customer_lookup_tool(self):
        """Create customer lookup function tool."""

        @function_tool
        async def lookup_customer_by_email(
            email: str,
        ) -> str:
            """
            Look up a customer by email address.

            Args:
                email: Customer email address

            Returns:
                Customer information or not found message
            """
            # This would need a session - for now return placeholder
            return f"Customer lookup for: {email} (requires database session)"

        return lookup_customer_by_email

    def _create_ticket_management_tool(self):
        """Create ticket management function tools."""

        @function_tool
        async def create_ticket(
            customer_id: str,
            subject: str,
            content: str,
            priority: str = "normal",
        ) -> str:
            """
            Create a new support ticket.

            Args:
                customer_id: Customer UUID
                subject: Ticket subject
                content: Ticket content/description
                priority: Priority level (low, normal, high, urgent)

            Returns:
                Ticket creation confirmation with ID
            """
            return f"Ticket created for customer {customer_id}: {subject}"

        @function_tool
        async def update_ticket_status(
            ticket_id: str,
            status: str,
        ) -> str:
            """
            Update ticket status.

            Args:
                ticket_id: Ticket UUID
                status: New status (open, in_progress, resolved, closed)

            Returns:
                Status update confirmation
            """
            return f"Ticket {ticket_id} status updated to: {status}"

        return [create_ticket, update_ticket_status]

    def _create_agent(self) -> Agent:
        """
        Create and configure the OpenAI Agent using ProviderManager.

        Returns:
            Configured Agent instance
        """
        # Gather all tools
        tools = []

        # Add knowledge retrieval skill (local knowledge base via pgvector)
        if self.config.enable_knowledge_retrieval:
            tools.append(knowledge_retrieval_skill)

        # Add search_knowledge_base tool (reads from product_info.txt)
        tools.append(search_knowledge_base)

        # Add Context7 external documentation search
        tools.append(external_docs_search)
        tools.append(multi_library_search)

        # Add human escalation tool
        tools.append(human_escalation)

        # Add customer lookup tool
        tools.append(self._create_customer_lookup_tool())

        # Add ticket management tools
        tools.extend(self._create_ticket_management_tool())

        # Create agent using ProviderManager (handles Gemini + fallback)
        # Try Gemini first, fallback to OpenRouter if rate limited
        try:
            agent = provider_manager.create_agent(
                name="Customer Success FTE",
                instructions="""
You are a Customer Success Digital FTE (Full-Time Equivalent) agent.
Your role is to provide 24/7 customer support across Email, WhatsApp, and Web channels.

*** CRITICAL INSTRUCTIONS ***
1. ALWAYS provide helpful, detailed responses - NEVER just say "I can't find information"
2. If knowledge base doesn't have the answer, use your general knowledge to help
3. Be conversational - understand context from previous messages
4. If user says "okay find" or similar, understand it as "please search" and respond helpfully
5. Provide value even without perfect information

*** CONTEXT PRIORIZATION ***
When you receive search results with "Context" or "Knowledge Base Results":
1. You MUST prioritize the provided Context above all else
2. If the answer is in the context, use it directly
3. The context contains authoritative information

Guidelines:
1. Be helpful, professional, and conversational
2. If knowledge base search returns no results, use your training knowledge
3. For pricing questions: Provide general pricing structures if exact numbers unavailable
4. For product questions: Describe typical features and benefits
5. For technical questions: Provide troubleshooting steps and best practices
6. Create tickets to track all customer interactions
7. Detect sentiment and escalate when needed

Tool Selection Guide:
- search_knowledge_base: Product info, pricing, plans, features, common issues
- knowledge_retrieval: Internal policies, procedures
- external_docs_search: Technical documentation
- multi_library_search: Multiple technical libraries
- human_escalation: When customer needs human agent
- lookup_customer_by_email: Find customer details
- create_ticket: Create support ticket
- update_ticket_status: Change ticket status

Response Style:
- Friendly and professional
- Concise but complete (2-4 paragraphs)
- Action-oriented (tell customer what to do next)
- Empathetic to customer concerns

Examples of GOOD responses:
- "While I don't have access to current pricing, typically our plans include... Let me connect you with sales for exact numbers."
- "Based on common practices for this product, you should... Here are the typical steps..."
- "I understand you're looking for [X]. While I search for specific details, here's what I can tell you..."

Escalation Criteria:
- Customer explicitly requests human agent
- Customer is frustrated/angry (negative sentiment < -0.5)
- Issue too complex or sensitive
- Billing/pricing requires human verification
- Legal or compliance issues

Always:
- Acknowledge customer concerns
- Provide clear, actionable information
- Offer follow-up assistance
- Document interactions in tickets
""",
                tools=tools,
                temperature=self.config.temperature,
            )
        except Exception as e:
            # Fallback to OpenRouter if Gemini fails
            logger.warning(f"Gemini failed, using OpenRouter fallback: {e}")
            agent = provider_manager.create_agent(
                name="Customer Success FTE",
                instructions="""
You are a Customer Success Digital FTE agent providing 24/7 support.
Be helpful, professional, and conversational.
Use the provided context to answer questions.
If context is missing, use your general knowledge.
""",
                tools=tools,
                temperature=self.config.temperature,
            )

        return agent

    async def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment of customer message.

        Uses direct rule-based analysis as primary method.
        Falls back to LiteLLM provider call if rule-based analysis fails.

        Args:
            text: Customer message text

        Returns:
            dict with score, emotion, and needs_escalation
        """
        if not self.config.enable_sentiment_analysis:
            return {
                "score": 0.0,
                "emotion": "neutral",
                "needs_escalation": False,
            }

        try:
            # Primary: Use direct rule-based sentiment service
            result = sentiment_service.analyze_sentiment_sync(text)
            return result
        except Exception as e:
            # Fallback: Use LiteLLM provider for sentiment analysis
            try:
                return await self._analyze_sentiment_litellm(text)
            except Exception as fallback_error:
                # Final fallback: Return neutral sentiment
                return {
                    "score": 0.0,
                    "emotion": "neutral",
                    "needs_escalation": False,
                    "error": str(fallback_error),
                }

    async def _analyze_sentiment_litellm(self, text: str) -> dict:
        """
        Fallback sentiment analysis using LiteLLM provider.

        Args:
            text: Text to analyze

        Returns:
            dict with score, emotion, and needs_escalation
        """
        sentiment_prompt = f"""
Analyze the sentiment of this customer message.
Return ONLY a valid JSON object with the following structure:
{{
    "score": <float from -1.0 (very negative) to 1.0 (very positive)>,
    "emotion": "<primary emotion: neutral, anger, frustration, disappointment, joy, satisfaction, gratitude>",
    "needs_escalation": <boolean>
}}

Message: {text}
"""
        try:
            result = await Runner.run(
                self.agent,
                sentiment_prompt,
                run_config=RunConfig(tracing_disabled=True),
            )
            # Parse JSON from result
            response_text = result.final_output.strip()
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                return {
                    "score": float(parsed.get("score", 0.0)),
                    "emotion": str(parsed.get("emotion", "neutral")),
                    "needs_escalation": bool(parsed.get("needs_escalation", False)),
                }
        except Exception:
            pass

        # Return neutral if parsing fails
        return {
            "score": 0.0,
            "emotion": "neutral",
            "needs_escalation": False,
        }

    def select_tool(self, query: str) -> ToolType:
        """
        Select appropriate tool for query.

        Args:
            query: User query text

        Returns:
            ToolType enum value
        """
        return tool_selector.select_tool(query)

    @property
    def agent(self) -> Agent:
        """Get or create the agent instance."""
        if self._agent is None:
            self._agent = self._create_agent()
        return self._agent

    async def generate_response(
        self,
        input_text: str,
        context: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Generate a response to customer input.

        Args:
            input_text: Customer message/question
            context: Optional context (customer info, ticket info, etc.)

        Returns:
            Generated response text
        """
        # Build input with context
        if context:
            input_with_context = f"""
Context:
{context}

Customer message: {input_text}
"""
        else:
            input_with_context = input_text

        # Run the agent with detailed error handling
        try:
            result = await Runner.run(
                self.agent,
                input_with_context,
                run_config=RunConfig(tracing_disabled=True),
            )
            return result.final_output
        except Exception as e:
            # Print detailed error for debugging
            error_type = type(e).__name__
            error_message = str(e)
            print(f"\n=== AGENT RUNTIME ERROR ===")
            print(f"Error Type: {error_type}")
            print(f"Error Message: {error_message}")
            print(f"Agent Model: {self.agent.model}")
            print(f"Agent Name: {self.agent.name}")
            print(f"Input Text: {input_text[:100]}...")
            print(f"==========================\n")
            
            # Re-raise with more context
            raise RuntimeError(f"Agent runtime error ({error_type}): {error_message}. Model: {self.agent.model}")


def create_fte_agent(config: Optional[FTEAgentConfig] = None) -> FTEAgent:
    """
    Factory function to create FTEAgent instance.

    Args:
        config: Optional agent configuration

    Returns:
        Configured FTEAgent instance
    """
    return FTEAgent(config=config)
