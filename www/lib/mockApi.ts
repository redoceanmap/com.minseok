export type Area = {
  id: string;
  name: string;
  lat: number;
  lng: number;
  category: string;
  reason: string;
  stats: {
    monthlyRevenueText: string;
    closureRateText: string;
    footTrafficText: string;
  };
};

const SEOUL_AREAS: Area[] = [
  {
    id: "seongsu",
    name: "성수동",
    lat: 37.5443,
    lng: 127.056,
    category: "카페·디저트",
    reason: "젊은 손님이 꾸준히 모이고 매출이 빠르게 늘어요",
    stats: {
      monthlyRevenueText: "한 달 평균 2,800만원 정도 벌어요",
      closureRateText: "폐업률은 6%로 낮은 편이에요",
      footTrafficText: "하루에 4만 2천 명이 지나가요",
    },
  },
  {
    id: "yeonnam",
    name: "연남동",
    lat: 37.5615,
    lng: 126.9237,
    category: "베이커리·브런치",
    reason: "주말 유동인구가 강하고 SNS 노출이 잘 돼요",
    stats: {
      monthlyRevenueText: "한 달 평균 2,300만원 정도 벌어요",
      closureRateText: "폐업률은 9%, 평균 수준이에요",
      footTrafficText: "주말엔 하루 5만 명이 다녀가요",
    },
  },
  {
    id: "mangwon",
    name: "망원동",
    lat: 37.5563,
    lng: 126.9106,
    category: "외식·동네 카페",
    reason: "임대료가 합리적이고 단골이 잘 붙어요",
    stats: {
      monthlyRevenueText: "한 달 평균 1,900만원 정도 벌어요",
      closureRateText: "폐업률은 7%로 안정적이에요",
      footTrafficText: "하루에 2만 8천 명이 지나가요",
    },
  },
];

export type AskResult = {
  text: string;
  recommendations: Area[];
};

export async function askMockAI(prompt: string): Promise<AskResult> {
  await new Promise((r) => setTimeout(r, 900));
  const picks = SEOUL_AREAS.slice(0, 3);
  const names = picks.map((p) => p.name).join(", ");
  return {
    text: `"${prompt.length > 30 ? prompt.slice(0, 30) + "…" : prompt}" 보고 골라봤어요. ${names} 세 곳이 괜찮아 보여요. 지도에서 어디인지 볼래요?`,
    recommendations: picks,
  };
}
