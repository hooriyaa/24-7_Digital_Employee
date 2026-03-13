"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { knowledgeBaseApi, KnowledgeBaseArticle } from "@/lib/api";
import { RefreshCw, Book, Tag } from "lucide-react";

export function KnowledgeBaseGrid() {
  const [articles, setArticles] = useState<KnowledgeBaseArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await knowledgeBaseApi.getAll();
      setArticles(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch articles");
      console.error("Error fetching articles:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, []);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">Knowledge Base</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            {articles.length} articles from database
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={fetchArticles}
          disabled={loading}
          className="gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          Refresh Data
        </Button>
      </div>

      {/* Error State */}
      {error && (
        <Card className="p-4 bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </Card>
      )}

      {/* Loading State */}
      {loading && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <Card key={i} className="h-48 animate-pulse bg-slate-100 dark:bg-slate-800" />
          ))}
        </div>
      )}

      {/* Articles Grid */}
      {!loading && !error && (
        <ScrollArea className="h-[600px]">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {articles.map((article) => (
              <Card
                key={article.id}
                className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
              >
                <div className="flex items-start gap-2 mb-2">
                  <Book className="h-5 w-5 text-slate-400 mt-0.5" />
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-slate-900 dark:text-slate-100 line-clamp-2">
                      {article.title}
                    </h3>
                  </div>
                </div>
                
                <div className="mb-3">
                  <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-3">
                    {article.content}
                  </p>
                </div>

                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="secondary" className="text-xs">
                    {article.category || "General"}
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    {article.source}
                  </Badge>
                </div>

                {article.tags && article.tags.length > 0 && (
                  <div className="flex items-center gap-1 flex-wrap">
                    <Tag className="h-3 w-3 text-slate-400" />
                    {article.tags.slice(0, 3).map((tag, i) => (
                      <span
                        key={i}
                        className="text-xs text-slate-500 dark:text-slate-400"
                      >
                        {tag}
                        {i < Math.min(article.tags.length - 1, 2) && ","}
                      </span>
                    ))}
                  </div>
                )}
              </Card>
            ))}
            {articles.length === 0 && (
              <Card className="col-span-full p-8 text-center">
                <p className="text-slate-500 dark:text-slate-400">
                  No articles found. Run the seed script to populate data.
                </p>
              </Card>
            )}
          </div>
        </ScrollArea>
      )}
    </div>
  );
}
