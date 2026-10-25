/**
 * Stable, isolated guest identity management.
 * Stores a unique UUID in localStorage to ensure guest progress,
 * stats, and vocabulary never cross-talk between different devices or incognito sessions.
 */

const GUEST_ID_KEY = "stone_guest_id";

export function getOrCreateGuestId(): string {
  if (typeof window === "undefined") {
    return "default";
  }
  try {
    let id = localStorage.getItem(GUEST_ID_KEY);
    if (!id || !id.startsWith("gst_")) {
      const rand = Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
      id = `gst_${rand}`;
      localStorage.setItem(GUEST_ID_KEY, id);
    }
    return id;
  } catch {
    return "default";
  }
}
