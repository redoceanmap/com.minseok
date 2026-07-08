"use client";

import { useState, useEffect } from "react";
import { X, ArrowLeft, Eye, EyeOff, Info } from "lucide-react";
import { useUIStore, type AuthMode } from "@/lib/uiStore";
import { api } from "@/lib/api";
import { setSession } from "@/lib/auth";

function PinMark({ size = 32 }: { size?: number }) {
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

function ToggleTabs({
  value,
  onChange,
}: {
  value: AuthMode;
  onChange: (v: AuthMode) => void;
}) {
  return (
    <div className="inline-flex bg-border/60 rounded-full p-1 text-sm font-medium">
      {(["login", "signup"] as const).map((m) => (
        <button
          key={m}
          type="button"
          onClick={() => onChange(m)}
          className={`px-6 py-1.5 rounded-full transition-colors ${
            value === m
              ? "bg-brand text-white"
              : "text-foreground-muted hover:text-foreground"
          }`}
        >
          {m === "login" ? "로그인" : "회원가입"}
        </button>
      ))}
    </div>
  );
}

function SnsButtons({ label }: { label: string }) {
  return (
    <div className="mt-6">
      <p className="text-center text-sm font-semibold text-foreground mb-3">
        {label}
      </p>
      <div className="flex items-center justify-center gap-3">
        <button
          type="button"
          aria-label="카카오로 시작"
          className="w-11 h-11 rounded-full bg-[#FEE500] grid place-items-center hover:opacity-90 transition-opacity"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="#000">
            <path d="M12 3C6.477 3 2 6.582 2 11c0 2.84 1.86 5.336 4.667 6.74l-1.18 4.293a.5.5 0 00.76.553L11.5 19.34a13.8 13.8 0 00.5.011c5.523 0 10-3.582 10-8.001S17.523 3 12 3z" />
          </svg>
        </button>
        <button
          type="button"
          aria-label="네이버로 시작"
          className="w-11 h-11 rounded-full bg-[#03C75A] grid place-items-center text-white font-bold text-base hover:opacity-90 transition-opacity"
        >
          N
        </button>
        <button
          type="button"
          aria-label="구글로 시작"
          className="w-11 h-11 rounded-full bg-white border border-border grid place-items-center hover:bg-black/[0.03] transition-colors"
        >
          <svg width="18" height="18" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
            <path fill="#FBBC04" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
          </svg>
        </button>
      </div>
    </div>
  );
}

const SIGNUP_TERMS = [
  { label: "(필수) 만 14세 이상입니다.", required: true },
  { label: "(필수) 이용약관 동의", required: true, link: true },
  { label: "(필수) 개인정보 수집 및 이용 동의", required: true, link: true },
  { label: "(선택) 마케팅 정보 수신 동의", required: false },
];

export default function AuthModal() {
  const open = useUIStore((s) => s.authOpen);
  const mode = useUIStore((s) => s.authMode);
  const setMode = useUIStore((s) => s.setAuthMode);
  const close = useUIStore((s) => s.closeAuth);
  const setUser = useUIStore((s) => s.setUser);

  const [state, setState] = useState({
    signupStep: "options" as "options" | "form",
    show: { pwd: false, pwd2: false },
    loading: false,
    error: null as string | null,
    success: null as string | null,
  });
  const { signupStep, show, loading, error, success } = state;

  useEffect(() => {
    if (open) {
      setState({ signupStep: "options", show: { pwd: false, pwd2: false }, loading: false, error: null, success: null });
    }
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

  const isSignupForm = mode === "signup" && signupStep === "form";

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setState(prev => ({ ...prev, error: null, loading: true }));
    const { email, password } = Object.fromEntries(new FormData(e.currentTarget)) as { email: string; password: string };
    try {
      const res = await api.login(email, password);
      setSession(res.access_token, { email: res.email, name: res.name });
      setUser({ name: res.name ?? res.email.split("@")[0] ?? "방문자" });
      close();
    } catch (err) {
      setState(prev => ({ ...prev, error: err instanceof Error ? err.message : "로그인에 실패했어요" }));
    } finally {
      setState(prev => ({ ...prev, loading: false }));
    }
  };

  const handleSignupSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setState(prev => ({ ...prev, error: null }));
    const { userId, password, password2, nickname, email } = Object.fromEntries(new FormData(e.currentTarget)) as { userId: string; password: string; password2: string; nickname: string; email: string };
    if (password !== password2) {
      setState(prev => ({ ...prev, error: "비밀번호가 일치하지 않아요" }));
      return;
    }
    setState(prev => ({ ...prev, loading: true }));
    try {
      await api.signup(userId, password, nickname, email);
      setState(prev => ({ ...prev, success: "가입이 완료됐어요. 이제 로그인하세요." }));
      setTimeout(() => setMode("login"), 1500);
    } catch (err) {
      setState(prev => ({ ...prev, error: err instanceof Error ? err.message : "회원가입에 실패했어요" }));
    } finally {
      setState(prev => ({ ...prev, loading: false }));
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm grid place-items-center px-4"
      onClick={close}
    >
      <div
        className="relative w-full max-w-md bg-surface rounded-2xl shadow-xl p-8 max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          type="button"
          onClick={close}
          aria-label="닫기"
          className="absolute top-4 right-4 w-8 h-8 grid place-items-center rounded-full text-foreground-muted hover:bg-black/5"
        >
          <X size={18} />
        </button>

        {isSignupForm && (
          <button
            type="button"
            onClick={() => setState(prev => ({ ...prev, signupStep: "options" }))}
            aria-label="뒤로"
            className="absolute top-4 left-4 w-8 h-8 grid place-items-center rounded-full text-foreground-muted hover:bg-black/5"
          >
            <ArrowLeft size={18} />
          </button>
        )}

        {!isSignupForm && (
          <div className="flex flex-col items-center mb-6">
            <PinMark size={36} />
            <span className="mt-2 text-lg font-semibold tracking-tight">
              redoceanmap
            </span>
          </div>
        )}

        <div className="flex justify-center mb-7">
          <ToggleTabs value={mode} onChange={setMode} />
        </div>

        {mode === "login" && (
          <form className="flex flex-col gap-3" onSubmit={handleLogin}>
            <input
              type="email"
              name="email"
              placeholder="이메일을 입력해주세요"
              required
              className="w-full bg-transparent border border-border rounded-xl px-4 py-3 text-sm outline-none focus:border-brand placeholder:text-foreground-muted"
            />
            <div className="relative">
              <input
                type={show.pwd ? "text" : "password"}
                name="password"
                placeholder="비밀번호를 입력해주세요"
                required
                className="w-full bg-transparent border border-border rounded-xl px-4 py-3 pr-10 text-sm outline-none focus:border-brand placeholder:text-foreground-muted"
              />
              <button
                type="button"
                onClick={() => setState(prev => ({ ...prev, show: { ...prev.show, pwd: !prev.show.pwd } }))}
                aria-label="비밀번호 표시"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-muted hover:text-foreground"
              >
                {show.pwd ? <Eye size={16} /> : <EyeOff size={16} />}
              </button>
            </div>

            {error && (
              <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl px-4 py-2">
                {error}
              </p>
            )}

            <div className="flex items-center justify-between mt-1 text-sm">
              <label className="flex items-center gap-2 text-foreground-muted cursor-pointer">
                <input type="checkbox" className="accent-brand" />
                로그인 유지
              </label>
              <button
                type="button"
                className="text-foreground-muted hover:text-foreground"
              >
                비밀번호 찾기
              </button>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-4 w-full bg-brand text-white py-3 rounded-xl font-medium hover:bg-brand-deep transition-colors disabled:opacity-50"
            >
              {loading ? "로그인 중..." : "로그인"}
            </button>

            <SnsButtons label="SNS 간편 로그인" />
          </form>
        )}

        {mode === "signup" && signupStep === "options" && (
          <div>
            <button
              type="button"
              onClick={() => setState(prev => ({ ...prev, signupStep: "form" }))}
              className="w-full border-2 border-brand text-brand font-medium py-3 rounded-xl hover:bg-brand/5 transition-colors"
            >
              이메일로 회원가입
            </button>
            <SnsButtons label="SNS 간편 가입" />
          </div>
        )}

        {isSignupForm && (
          <form className="flex flex-col gap-4" onSubmit={handleSignupSubmit}>
            <div>
              <label className="block text-sm font-semibold mb-2">아이디</label>
              <input
                type="text"
                name="userId"
                placeholder="아이디를 입력해주세요"
                required
                className="w-full bg-transparent border border-border rounded-xl px-4 py-3 text-sm outline-none focus:border-brand placeholder:text-foreground-muted"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">닉네임</label>
              <input
                type="text"
                name="nickname"
                placeholder="닉네임을 입력해주세요"
                required
                className="w-full bg-transparent border border-border rounded-xl px-4 py-3 text-sm outline-none focus:border-brand placeholder:text-foreground-muted"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">이메일</label>
              <input
                type="email"
                name="email"
                placeholder="이메일을 입력해주세요"
                required
                className="w-full bg-transparent border border-border rounded-xl px-4 py-3 text-sm outline-none focus:border-brand placeholder:text-foreground-muted"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">
                비밀번호
              </label>
              <div className="relative mb-2">
                <input
                  type={show.pwd ? "text" : "password"}
                  name="password"
                  placeholder="비밀번호를 입력해주세요"
                  required
                  className="w-full bg-transparent border border-border rounded-xl px-4 py-3 pr-10 text-sm outline-none focus:border-brand placeholder:text-foreground-muted"
                />
                <button
                  type="button"
                  onClick={() => setState(prev => ({ ...prev, show: { ...prev.show, pwd: !prev.show.pwd } }))}
                  aria-label="비밀번호 표시"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-muted hover:text-foreground"
                >
                  {show.pwd ? <Eye size={16} /> : <EyeOff size={16} />}
                </button>
              </div>
              <div className="relative">
                <input
                  type={show.pwd2 ? "text" : "password"}
                  name="password2"
                  placeholder="비밀번호를 다시 입력해주세요"
                  required
                  className="w-full bg-transparent border border-border rounded-xl px-4 py-3 pr-10 text-sm outline-none focus:border-brand placeholder:text-foreground-muted"
                />
                <button
                  type="button"
                  onClick={() => setState(prev => ({ ...prev, show: { ...prev.show, pwd2: !prev.show.pwd2 } }))}
                  aria-label="비밀번호 표시"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-muted hover:text-foreground"
                >
                  {show.pwd2 ? <Eye size={16} /> : <EyeOff size={16} />}
                </button>
              </div>
              <p className="mt-2 text-xs text-foreground-muted flex items-center gap-1.5">
                <Info size={13} strokeWidth={1.75} />
                영문 대소문자 · 숫자 · 특수문자 중 2가지 이상 조합 (8자~64자)
              </p>
            </div>

            <div className="mt-2 flex flex-col gap-2 text-sm">
              <label className="flex items-center gap-2 font-semibold cursor-pointer">
                <input type="checkbox" className="accent-brand" />
                전체 동의합니다.
              </label>
              {SIGNUP_TERMS.map((t) => (
                <label
                  key={t.label}
                  className="flex items-center gap-2 text-foreground-muted cursor-pointer pl-5"
                >
                  <input type="checkbox" className="accent-brand" />
                  {t.link ? (
                    <span>
                      {t.label.split(/(이용약관|개인정보 수집 및 이용)/).map((part, i) =>
                        part === "이용약관" || part === "개인정보 수집 및 이용" ? (
                          <span key={i} className="underline">
                            {part}
                          </span>
                        ) : (
                          <span key={i}>{part}</span>
                        )
                      )}
                    </span>
                  ) : (
                    t.label
                  )}
                </label>
              ))}
            </div>

            {success && (
              <p className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-xl px-4 py-2">
                {success}
              </p>
            )}

            {error && (
              <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl px-4 py-2">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading || !!success}
              className="mt-4 w-full bg-brand text-white py-3 rounded-xl font-medium hover:bg-brand-deep transition-colors disabled:opacity-50"
            >
              {loading ? "가입 중..." : "가입하기"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
