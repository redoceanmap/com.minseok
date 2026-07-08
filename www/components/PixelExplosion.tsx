export default function PixelExplosion({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 80 80"
      shapeRendering="crispEdges"
      className={className}
      aria-hidden
    >
      {/* 외곽 파편 (빨강) - 8방향 끝점 */}
      <rect x="36" y="0" width="8" height="8" fill="#E94560" />
      <rect x="36" y="72" width="8" height="8" fill="#E94560" />
      <rect x="0" y="36" width="8" height="8" fill="#E94560" />
      <rect x="72" y="36" width="8" height="8" fill="#E94560" />
      <rect x="12" y="12" width="8" height="8" fill="#E94560" />
      <rect x="60" y="12" width="8" height="8" fill="#E94560" />
      <rect x="12" y="60" width="8" height="8" fill="#E94560" />
      <rect x="60" y="60" width="8" height="8" fill="#E94560" />

      {/* 추가 파편 - 작은 점들 (불꽃 튐) */}
      <rect x="24" y="4" width="4" height="4" fill="#E94560" />
      <rect x="52" y="4" width="4" height="4" fill="#E94560" />
      <rect x="4" y="24" width="4" height="4" fill="#E94560" />
      <rect x="72" y="24" width="4" height="4" fill="#E94560" />
      <rect x="4" y="52" width="4" height="4" fill="#E94560" />
      <rect x="72" y="52" width="4" height="4" fill="#E94560" />
      <rect x="24" y="72" width="4" height="4" fill="#E94560" />
      <rect x="52" y="72" width="4" height="4" fill="#E94560" />

      {/* 십자 파편 (주황) - 본체 줄기 */}
      <rect x="36" y="8" width="8" height="64" fill="#FF6B35" />
      <rect x="8" y="36" width="64" height="8" fill="#FF6B35" />

      {/* 대각선 파편 (주황) */}
      <rect x="20" y="20" width="8" height="8" fill="#FF6B35" />
      <rect x="52" y="20" width="8" height="8" fill="#FF6B35" />
      <rect x="20" y="52" width="8" height="8" fill="#FF6B35" />
      <rect x="52" y="52" width="8" height="8" fill="#FF6B35" />

      {/* 별 본체 - 노랑 (다이아몬드형) */}
      <rect x="32" y="16" width="16" height="48" fill="#FFC857" />
      <rect x="16" y="32" width="48" height="16" fill="#FFC857" />
      <rect x="24" y="24" width="32" height="32" fill="#FFC857" />

      {/* 별 안쪽 - 밝은 노랑 */}
      <rect x="36" y="20" width="8" height="40" fill="#FFE873" />
      <rect x="20" y="36" width="40" height="8" fill="#FFE873" />
      <rect x="28" y="28" width="24" height="24" fill="#FFE873" />

      {/* 핵심 - 흰색/뜨거운 빛 */}
      <rect x="32" y="32" width="16" height="16" fill="#FFFAE3" />
      <rect x="36" y="28" width="8" height="24" fill="#FFFAE3" />
      <rect x="28" y="36" width="24" height="8" fill="#FFFAE3" />
    </svg>
  );
}
