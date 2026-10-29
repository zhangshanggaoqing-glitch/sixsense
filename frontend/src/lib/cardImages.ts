/**
 * High-quality, copyright-free landscape background images for punch cards.
 * Features 10 curated local static assets (nature, mountains, ocean, mist, calm light)
 * with Unsplash external fallbacks to prevent any CORS or network issues.
 */

export interface CardBgItem {
  id: string;
  localUrl: string;
  unsplashUrl: string;
  theme: "dark" | "light"; // Theme determines text contrast (all our chosen bgs are atmospheric dark/medium)
}

export const CARD_BACKGROUNDS: CardBgItem[] = [
  {
    id: "bg-1",
    localUrl: "/card-bg/bg-1.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-2",
    localUrl: "/card-bg/bg-2.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-3",
    localUrl: "/card-bg/bg-3.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-4",
    localUrl: "/card-bg/bg-4.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1426604966848-d7adac402bff?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-5",
    localUrl: "/card-bg/bg-5.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-6",
    localUrl: "/card-bg/bg-6.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-7",
    localUrl: "/card-bg/bg-7.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-8",
    localUrl: "/card-bg/bg-8.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-9",
    localUrl: "/card-bg/bg-9.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
  {
    id: "bg-10",
    localUrl: "/card-bg/bg-10.jpg",
    unsplashUrl: "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?auto=format&fit=crop&w=1080&h=1440&q=80",
    theme: "dark",
  },
];

/**
 * Deterministically pick a background image for a given date string (YYYY-MM-DD),
 * rotating across days while remaining consistent throughout the same day.
 */
export function getDailyBg(dateStr?: string): CardBgItem {
  if (!dateStr) {
    const now = new Date();
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    const cst = new Date(utc + 3600000 * 8);
    dateStr = `${cst.getFullYear()}-${String(cst.getMonth() + 1).padStart(2, "0")}-${String(cst.getDate()).padStart(2, "0")}`;
  }

  let hash = 0;
  for (let i = 0; i < dateStr.length; i++) {
    hash = (hash << 5) - hash + dateStr.charCodeAt(i);
    hash |= 0;
  }
  const index = Math.abs(hash) % CARD_BACKGROUNDS.length;
  return CARD_BACKGROUNDS[index];
}
