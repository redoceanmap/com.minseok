"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { useChatStore } from "@/lib/store";
import MapView from "@/components/seoul/MapView";
import RecommendDetail from "@/components/seoul/RecommendDetail";

export default function MapPage() {
  const recommendations = useChatStore((s) => s.recommendations);
  const [state, setState] = useState<{ selectedId: string | null; tab: "map" | "detail" }>({
    selectedId: null,
    tab: "map",
  });

  useEffect(() => {
    if (!state.selectedId && recommendations.length > 0) {
      setState((prev) => ({ ...prev, selectedId: recommendations[0].id }));
    }
  }, [recommendations, state.selectedId]);

  const selected = recommendations.find((a) => a.id === state.selectedId) ?? null;

  const handleSelect = (id: string) => {
    setState({ selectedId: id, tab: "detail" });
  };

  if (recommendations.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center px-6 text-center gap-4">
        <p className="text-foreground-muted">아직 추천받은 동네가 없어요</p>
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand text-white text-sm font-medium hover:bg-brand-deep transition-colors"
        >
          <ArrowLeft size={15} strokeWidth={2.25} />
          대화로 돌아가기
        </Link>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col min-h-0 px-4 md:px-6 pb-4 md:pb-6">
      <div className="flex items-center justify-between mb-3 md:mb-4">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm text-foreground-muted hover:text-foreground"
        >
          <ArrowLeft size={15} strokeWidth={1.75} />
          대화로 돌아가기
        </Link>
        <div className="text-xs text-foreground-muted">추천 {recommendations.length}곳</div>
      </div>

      {/* 모바일 탭 전환 */}
      <div className="lg:hidden flex rounded-xl border border-border overflow-hidden mb-3 text-sm font-medium">
        <button
          type="button"
          onClick={() => setState((prev) => ({ ...prev, tab: "map" }))}
          className={`flex-1 py-2 transition-colors ${
            state.tab === "map"
              ? "bg-brand text-white"
              : "bg-surface text-foreground-muted hover:text-foreground"
          }`}
        >
          지도
        </button>
        <button
          type="button"
          onClick={() => setState((prev) => ({ ...prev, tab: "detail" }))}
          className={`flex-1 py-2 transition-colors ${
            state.tab === "detail"
              ? "bg-brand text-white"
              : "bg-surface text-foreground-muted hover:text-foreground"
          }`}
        >
          상세 정보
        </button>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-4 min-h-0">
        <div
          className={`min-h-[420px] lg:min-h-0 ${
            state.tab === "detail" ? "hidden lg:block" : "block"
          }`}
        >
          <MapView
            areas={recommendations}
            selectedId={state.selectedId}
            onSelect={handleSelect}
          />
        </div>
        <aside
          className={`bg-surface border border-border rounded-2xl overflow-hidden ${
            state.tab === "map" ? "hidden lg:block" : "block"
          }`}
        >
          <RecommendDetail area={selected} />
        </aside>
      </div>
    </div>
  );
}
