/**
 * 石头听力 - 客户端认证与用户状态持久化工具
 */

export interface User {
  id: string;
  username: string;
  created_at?: number;
  is_admin?: boolean;
}

const TOKEN_KEY = "sixsense_auth_token";
const USER_KEY = "sixsense_auth_user";

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export function getStoredUser(): User | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(USER_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as User;
  } catch {
    return null;
  }
}

export function setStoredAuth(token: string, user: User): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    window.dispatchEvent(new Event("sixsense-auth-changed"));
  } catch (e) {
    console.error("Failed to save auth to localStorage", e);
  }
}

export function clearStoredAuth(): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    window.dispatchEvent(new Event("sixsense-auth-changed"));
  } catch (e) {
    console.error("Failed to clear auth from localStorage", e);
  }
}
