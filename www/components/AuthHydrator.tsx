"use client";

import { useEffect } from "react";
import { getProfile, getToken } from "@/lib/auth";
import { useUIStore } from "@/lib/uiStore";

export default function AuthHydrator() {
  const setUser = useUIStore((s) => s.setUser);

  useEffect(() => {
    if (!getToken()) return;
    const p = getProfile();
    if (!p) return;
    const name = p.name ?? p.email?.split("@")[0] ?? "방문자";
    setUser({ name });
  }, [setUser]);

  return null;
}
