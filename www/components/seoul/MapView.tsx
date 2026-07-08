"use client";

import type { Area } from "@/lib/mockApi";

const SEOUL_BBOX = {
  minLat: 37.42,
  maxLat: 37.7,
  minLng: 126.76,
  maxLng: 127.18,
};

function projectToPercent(lat: number, lng: number) {
  const x =
    ((lng - SEOUL_BBOX.minLng) / (SEOUL_BBOX.maxLng - SEOUL_BBOX.minLng)) * 100;
  const y =
    (1 - (lat - SEOUL_BBOX.minLat) / (SEOUL_BBOX.maxLat - SEOUL_BBOX.minLat)) *
    100;
  return { x, y };
}

type Props = {
  areas: Area[];
  selectedId: string | null;
  onSelect: (id: string) => void;
};

export default function MapView({ areas, selectedId, onSelect }: Props) {
  return (
    <div className="relative w-full h-full rounded-2xl overflow-hidden border border-border bg-[#F2EEE6]">
      <div
        aria-hidden
        className="absolute inset-0 opacity-60"
        style={{
          backgroundImage:
            "linear-gradient(to right, rgba(114,47,55,0.06) 1px, transparent 1px), linear-gradient(to bottom, rgba(114,47,55,0.06) 1px, transparent 1px)",
          backgroundSize: "40px 40px",
        }}
      />

      <div className="absolute top-3 left-3 text-xs text-foreground-muted bg-surface/80 backdrop-blur px-2.5 py-1 rounded-full border border-border">
        서울 · 임시 지도 (카카오맵 키 들어오면 교체)
      </div>

      {areas.map((area) => {
        const { x, y } = projectToPercent(area.lat, area.lng);
        const isActive = area.id === selectedId;
        return (
          <button
            key={area.id}
            onClick={() => onSelect(area.id)}
            className="absolute -translate-x-1/2 -translate-y-full group"
            style={{ left: `${x}%`, top: `${y}%` }}
            aria-label={`${area.name} 마커`}
          >
            <div
              className={`flex flex-col items-center transition-all ${
                isActive ? "scale-110" : "group-hover:scale-105"
              }`}
            >
              <span
                className={`px-2 py-1 rounded-md text-xs font-semibold mb-1 shadow-sm whitespace-nowrap ${
                  isActive
                    ? "bg-brand text-white"
                    : "bg-surface text-foreground border border-border"
                }`}
              >
                {area.name}
              </span>
              <svg
                width="22"
                height="28"
                viewBox="0 0 16 20"
                aria-hidden
                className="drop-shadow"
              >
                <path
                  d="M8 0C3.6 0 0 3.6 0 8c0 6 8 12 8 12s8-6 8-12c0-4.4-3.6-8-8-8z"
                  fill={isActive ? "#4A1D24" : "#722F37"}
                />
                <circle cx="8" cy="8" r="2.8" fill="#FAF7F2" />
              </svg>
            </div>
          </button>
        );
      })}

      {areas.length === 0 && (
        <div className="absolute inset-0 grid place-items-center text-sm text-foreground-muted">
          추천받은 동네가 아직 없어요
        </div>
      )}
    </div>
  );
}
