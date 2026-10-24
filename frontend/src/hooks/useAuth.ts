"use client";

import { useState, useEffect, useCallback } from "react";
import { User, getStoredToken, getStoredUser, setStoredAuth, clearStoredAuth } from "@/lib/auth";
import { api } from "@/lib/api";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    const token = getStoredToken();
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }
    const cachedUser = getStoredUser();
    if (cachedUser) {
      setUser(cachedUser);
    }
    try {
      const me = await api.getMe();
      if (me) {
        setUser(me);
        setStoredAuth(token, me);
      } else {
        clearStoredAuth();
        setUser(null);
      }
    } catch {
      // offline or network hiccup, keep cached user
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshUser();
    const handleAuthChange = () => {
      setUser(getStoredUser());
    };
    window.addEventListener("sixsense-auth-changed", handleAuthChange);
    return () => window.removeEventListener("sixsense-auth-changed", handleAuthChange);
  }, [refreshUser]);

  const login = async (username: string, password: string) => {
    const res = await api.login(username, password, true);
    setStoredAuth(res.token, res.user);
    setUser(res.user);
    return res.user;
  };

  const register = async (username: string, password: string) => {
    const res = await api.register(username, password, true);
    setStoredAuth(res.token, res.user);
    setUser(res.user);
    return res.user;
  };

  const logout = () => {
    clearStoredAuth();
    setUser(null);
  };

  return {
    user,
    isLoggedIn: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
  };
}
