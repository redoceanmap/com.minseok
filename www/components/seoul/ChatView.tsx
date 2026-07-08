"use client";

import Link from "next/link";
import { useChatStore } from "@/lib/store";
import { Map as MapIcon } from "lucide-react";

function PinMark({ size = 14 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={Math.round((size * 20) / 16)}
      viewBox="0 0 16 20"
      aria-hidden
    >
      <path
        d="M8 0C3.6 0 0 3.6 0 8c0 6 8 12 8 12s8-6 8-12c0-4.4-3.6-8-8-8z"
        fill="#722F37"
      />
      <circle cx="8" cy="8" r="2.5" fill="#FAF7F2" />
    </svg>
  );
}

export default function ChatView() {
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);

  return (
    <div className="w-full max-w-3xl mx-auto flex flex-col gap-6 py-8">
      {messages.map((m) => {
        if (m.role === "user") {
          return (
            <div key={m.id} className="flex justify-end">
              <div className="max-w-[80%] bg-surface border border-border rounded-2xl px-4 py-3 text-foreground whitespace-pre-wrap">
                {m.content}
              </div>
            </div>
          );
        }
        return (
          <div key={m.id} className="flex gap-3">
            <div className="shrink-0 w-7 h-7 grid place-items-center pt-1">
              <PinMark />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-foreground leading-relaxed whitespace-pre-wrap">
                {m.content}
              </p>

              {m.recommendations && m.recommendations.length > 0 && (
                <>
                  <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-2">
                    {m.recommendations.map((r) => (
                      <div
                        key={r.id}
                        className="bg-surface border border-border rounded-lg p-3"
                      >
                        <div className="text-sm font-semibold">{r.name}</div>
                        <div className="text-xs text-foreground-muted mt-0.5">
                          {r.category}
                        </div>
                        <p className="text-xs mt-2 text-foreground/80 leading-snug">
                          {r.reason}
                        </p>
                      </div>
                    ))}
                  </div>
                  <Link
                    href="/map"
                    className="mt-3 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand text-white text-sm font-medium hover:bg-brand-deep transition-colors"
                  >
                    <MapIcon size={15} strokeWidth={2} />
                    지도에서 볼래요?
                  </Link>
                </>
              )}
            </div>
          </div>
        );
      })}

      {isLoading && (
        <div className="flex gap-3 items-center">
          <div className="shrink-0 w-7 h-7 grid place-items-center pt-1">
            <PinMark />
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-brand animate-bounce [animation-delay:-0.3s]" />
            <span className="w-1.5 h-1.5 rounded-full bg-brand animate-bounce [animation-delay:-0.15s]" />
            <span className="w-1.5 h-1.5 rounded-full bg-brand animate-bounce" />
            <span className="ml-2 text-sm text-foreground-muted">
              동네를 살펴보고 있어요
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
