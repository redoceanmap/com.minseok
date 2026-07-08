export default function PixelIceberg({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 80 36"
      shapeRendering="crispEdges"
      className={className}
      aria-hidden
    >
      {/* 빙산 본체 - 뾰족하고 들쭉날쭉한 비대칭 봉우리 */}
      <rect x="32" y="0" width="4" height="4" fill="#B8D4E3" />
      <rect x="28" y="4" width="12" height="4" fill="#B8D4E3" />
      <rect x="24" y="8" width="20" height="4" fill="#B8D4E3" />
      <rect x="24" y="12" width="28" height="4" fill="#B8D4E3" />
      <rect x="16" y="16" width="36" height="4" fill="#B8D4E3" />
      <rect x="12" y="20" width="44" height="4" fill="#B8D4E3" />
      <rect x="8" y="24" width="52" height="4" fill="#B8D4E3" />
      <rect x="8" y="28" width="56" height="4" fill="#B8D4E3" />

      {/* 그림자 면 (오른쪽 슬로프 - 비대칭 절벽) */}
      <rect x="36" y="4" width="4" height="4" fill="#6FA0BC" />
      <rect x="40" y="8" width="4" height="4" fill="#6FA0BC" />
      <rect x="44" y="12" width="8" height="4" fill="#6FA0BC" />
      <rect x="48" y="16" width="4" height="4" fill="#6FA0BC" />
      <rect x="52" y="20" width="4" height="4" fill="#6FA0BC" />
      <rect x="56" y="24" width="4" height="4" fill="#6FA0BC" />
      <rect x="60" y="28" width="4" height="4" fill="#6FA0BC" />

      {/* 그림자 깊은 부분 - 절벽 음영 */}
      <rect x="48" y="12" width="4" height="4" fill="#4A7A98" />
      <rect x="60" y="24" width="4" height="4" fill="#4A7A98" />

      {/* 하이라이트 (왼쪽 위, 빛 받는 면) */}
      <rect x="32" y="0" width="2" height="2" fill="#F0EFE7" />
      <rect x="28" y="4" width="4" height="2" fill="#F0EFE7" />
      <rect x="24" y="8" width="4" height="2" fill="#F0EFE7" />
      <rect x="16" y="16" width="4" height="2" fill="#F0EFE7" />

      {/* 표면 균열/크랙 디테일 */}
      <rect x="32" y="16" width="2" height="2" fill="#9BBED1" />
      <rect x="20" y="24" width="2" height="2" fill="#9BBED1" />
      <rect x="40" y="20" width="2" height="2" fill="#9BBED1" />

      {/* 수면 아래 살짝 비치는 부분 */}
      <rect x="12" y="32" width="48" height="2" fill="#7AA8C7" opacity="0.6" />
      <rect x="16" y="34" width="40" height="2" fill="#7AA8C7" opacity="0.35" />
    </svg>
  );
}
