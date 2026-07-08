import { create } from "zustand";
import { askMockAI, type Area } from "./mockApi";

export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  recommendations?: Area[];
};

type ChatState = {
  messages: Message[];
  recommendations: Area[];
  isLoading: boolean;
  sendMessage: (prompt: string) => Promise<void>;
  reset: () => void;
};

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  recommendations: [],
  isLoading: false,
  sendMessage: async (prompt) => {
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: prompt,
    };
    set((s) => ({ messages: [...s.messages, userMsg], isLoading: true }));

    const { text, recommendations } = await askMockAI(prompt);

    const aiMsg: Message = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: text,
      recommendations,
    };
    set((s) => ({
      messages: [...s.messages, aiMsg],
      recommendations,
      isLoading: false,
    }));
  },
  reset: () => set({ messages: [], recommendations: [], isLoading: false }),
}));
