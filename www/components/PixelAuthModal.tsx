"use client";

import { useEffect, useState } from "react";
import { useUIStore, type AuthMode } from "@/lib/uiStore";
import { api } from "@/lib/api";
import { setSession } from "@/lib/auth";

function PixelTabs({
  value,
  onChange,
}: {
  value: AuthMode;
  onChange: (v: AuthMode) => void;
}) {
  return (
    <div className="inline-flex border-4 border-accent bg-night-deep p-1">
      {(["login", "signup"] as const).map((m) => (
        <button
          key={m}
          type="button"
          onClick={() => onChange(m)}
          className={`pixel-text text-[10px] px-4 py-2 transition-colors ${
            value === m
              ? "bg-accent text-hull"
              : "text-accent hover:bg-night-mid"
          }`}
        >
          {m === "login" ? "LOGIN" : "JOIN"}
        </button>
      ))}
    </div>
  );
}

function PixelInput({
  label,
  type = "text",
  name,
  placeholder,
  required,
}: {
  label: string;
  type?: string;
  name: string;
  placeholder?: string;
  required?: boolean;
}) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="pixel-text text-[9px] text-accent">{label}</span>
      <input
        type={type}
        name={name}
        placeholder={placeholder}
        required={required}
        className="bg-night-deep border-4 border-accent px-3 py-2.5 text-ink text-sm font-sans outline-none focus:border-glow placeholder:text-muted"
      />
    </label>
  );
}

export default function PixelAuthModal() {
  const open = useUIStore((s) => s.authOpen);
  const mode = useUIStore((s) => s.authMode);
  const setMode = useUIStore((s) => s.setAuthMode);
  const close = useUIStore((s) => s.closeAuth);
  const setUser = useUIStore((s) => s.setUser);

  const [ui, setUi] = useState<{ loading: boolean; error: string | null; notice: string | null }>({
    loading: false,
    error: null,
    notice: null,
  });

  useEffect(() => {
    if (open) setUi({ loading: false, error: null, notice: null });
  }, [open, mode]);

  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, close]);

  if (!open) return null;

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setUi(prev => ({ ...prev, error: null, loading: true }));
    const data = Object.fromEntries(new FormData(e.currentTarget)) as { email: string; password: string };
    try {
      const res = await api.login(data.email, data.password);
      setSession(res.access_token, { email: res.email, name: res.name });
      setUser({ name: res.name ?? res.email.split("@")[0] ?? "방문자" });
      close();
    } catch (err) {
      setUi(prev => ({ ...prev, error: err instanceof Error ? err.message : "로그인에 실패했어요" }));
    } finally {
      setUi(prev => ({ ...prev, loading: false }));
    }
  };

  const handleSignup = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setUi(prev => ({ ...prev, error: null, notice: null, loading: true }));
    const data = Object.fromEntries(new FormData(e.currentTarget)) as { userId: string; password: string; nickname: string; email: string };
    try {
      await api.signup(data.userId, data.password, data.nickname, data.email);
      setUi(prev => ({ ...prev, notice: "가입이 완료됐어요. 이제 로그인하세요." }));
      setMode("login");
    } catch (err) {
      setUi(prev => ({ ...prev, error: err instanceof Error ? err.message : "회원가입에 실패했어요" }));
    } finally {
      setUi(prev => ({ ...prev, loading: false }));
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 bg-black/70 grid place-items-center px-4"
      onClick={close}
    >
      <div
        className="relative w-full max-w-md bg-hull border-4 border-accent shadow-pixel-lg"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="bg-accent px-3 py-2 border-b-4 border-black flex items-center justify-between">
          <span className="pixel-text text-[10px] text-hull">
            ▼ {mode === "login" ? "FIRST CLASS · CABIN" : "TICKET · BOARDING PASS"}
          </span>
          <button
            type="button"
            onClick={close}
            aria-label="닫기"
            className="pixel-text text-[10px] text-hull hover:text-hull/70"
          >
            [ X ]
          </button>
        </div>

        <div className="p-6 sm:p-8">
          <div className="flex flex-col items-center mb-6">
            <span className="pixel-text text-2xl text-accent text-shadow-glow animate-flicker">
              TITANIC
            </span>
            <span className="pixel-text text-[8px] text-accent/70 mt-2">
              ★ APRIL 14, 1912 ★
            </span>
          </div>

          <div className="flex justify-center mb-6">
            <PixelTabs value={mode} onChange={setMode} />
          </div>

          {ui.notice && (
            <p className="pixel-text text-[9px] text-glow bg-night-deep border-4 border-glow px-3 py-2 mb-4">
              {ui.notice}
            </p>
          )}

          {mode === "login" ? (
            <form onSubmit={handleLogin} className="flex flex-col gap-4">
              <PixelInput
                label="EMAIL"
                type="email"
                name="email"
                placeholder="captain@titanic.com"
                required
              />
              <PixelInput
                label="PASSWORD"
                type="password"
                name="password"
                placeholder="••••••••"
                required
              />
              {ui.error && (
                <p className="pixel-text text-[9px] text-hull bg-glow border-4 border-black px-3 py-2">
                  ! {ui.error}
                </p>
              )}
              <button
                type="submit"
                disabled={ui.loading}
                className="mt-2 pixel-text text-xs text-hull bg-accent border-4 border-black px-4 py-3 shadow-pixel-sm hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all disabled:opacity-50"
              >
                {ui.loading ? "..." : "BOARD THE SHIP"}
              </button>
            </form>
          ) : (
            <form onSubmit={handleSignup} className="flex flex-col gap-4">
              <PixelInput
                label="USER ID"
                name="userId"
                placeholder="captain01"
                required
              />
              <PixelInput
                label="NICKNAME"
                name="nickname"
                placeholder="이름"
                required
              />
              <PixelInput
                label="EMAIL"
                type="email"
                name="email"
                placeholder="captain@titanic.com"
                required
              />
              <PixelInput
                label="PASSWORD"
                type="password"
                name="password"
                placeholder="••••••••"
                required
              />
              {ui.error && (
                <p className="pixel-text text-[9px] text-hull bg-glow border-4 border-black px-3 py-2">
                  ! {ui.error}
                </p>
              )}
              <button
                type="submit"
                disabled={ui.loading}
                className="mt-2 pixel-text text-xs text-hull bg-gradient-to-b from-accent to-accent-hover border-4 border-black px-4 py-3 shadow-glow hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-pixel-sm transition-all disabled:opacity-50"
              >
                {ui.loading ? "..." : "CLAIM YOUR TICKET"}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
