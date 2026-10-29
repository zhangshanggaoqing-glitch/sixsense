/**
 * Curated public domain / free-to-use inspirational & philosophical English quotes
 * Designed for minimalist Apple-style study cards (spacious typography, timeless meaning).
 */

export interface QuoteItem {
  text: string;
  author: string;
}

export const CURATED_QUOTES: QuoteItem[] = [
  { text: "The secret of getting ahead is getting started.", author: "Mark Twain" },
  { text: "It does not matter how slowly you go as long as you do not stop.", author: "Confucius" },
  { text: "We are what we repeatedly do. Excellence, then, is not an act, but a habit.", author: "Will Durant" },
  { text: "Dwell on the beauty of life. Watch the stars, and see yourself running with them.", author: "Marcus Aurelius" },
  { text: "He who has a why to live can bear almost any how.", author: "Friedrich Nietzsche" },
  { text: "What you get by achieving your goals is not as important as what you become.", author: "Henry David Thoreau" },
  { text: "The only limit to our realization of tomorrow will be our doubts of today.", author: "Franklin D. Roosevelt" },
  { text: "In the middle of difficulty lies opportunity.", author: "Albert Einstein" },
  { text: "Small deeds done are better than great deeds planned.", author: "Peter Marshall" },
  { text: "Keep your face always toward the sunshine, and shadows will fall behind you.", author: "Walt Whitman" },
  { text: "The journey of a thousand miles begins with a single step.", author: "Lao Tzu" },
  { text: "Do what you can, with what you have, where you are.", author: "Theodore Roosevelt" },
  { text: "Wisdom begins in wonder.", author: "Socrates" },
  { text: "Nature does not hurry, yet everything is accomplished.", author: "Lao Tzu" },
  { text: "Simplicity is the ultimate sophistication.", author: "Leonardo da Vinci" },
  { text: "Life is really simple, but we insist on making it complicated.", author: "Confucius" },
  { text: "The best way out is always through.", author: "Robert Frost" },
  { text: "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", author: "Ralph Waldo Emerson" },
  { text: "Nothing great was ever achieved without enthusiasm.", author: "Ralph Waldo Emerson" },
  { text: "Action is the foundational key to all success.", author: "Pablo Picasso" },
  { text: "Continuous effort, not strength or intelligence, is the key to unlocking our potential.", author: "Winston Churchill" },
  { text: "Perseverance is failing 19 times and succeeding the 20th.", author: "Julie Andrews" },
  { text: "Courage is grace under pressure.", author: "Ernest Hemingway" },
  { text: "Difficulties strengthen the mind, as labor does the body.", author: "Seneca" },
  { text: "A smooth sea never made a skilled sailor.", author: "Franklin D. Roosevelt" },
  { text: "Turn your wounds into wisdom.", author: "Oprah Winfrey" },
  { text: "Patience and perseverance have a magical effect before which difficulties disappear.", author: "John Quincy Adams" },
  { text: "Success is the sum of small efforts, repeated day in and day out.", author: "Robert Collier" },
  { text: "Every morning we are born again. What we do today is what matters most.", author: "Buddha" },
  { text: "The future belongs to those who believe in the beauty of their dreams.", author: "Eleanor Roosevelt" },
  { text: "What we achieve inwardly will change outer reality.", author: "Plutarch" },
  { text: "There is nothing impossible to him who will try.", author: "Alexander the Great" },
  { text: "Genius is one percent inspiration and ninety-nine percent perspiration.", author: "Thomas Edison" },
  { text: "The roots of education are bitter, but the fruit is sweet.", author: "Aristotle" },
  { text: "Learning never exhausts the mind.", author: "Leonardo da Vinci" },
  { text: "If you want to fly, you have to give up the things that weigh you down.", author: "Toni Morrison" },
  { text: "Everything has beauty, but not everyone sees it.", author: "Confucius" },
  { text: "Light tomorrow with today.", author: "Elizabeth Barrett Browning" },
  { text: "Step by step the longest march can be won.", author: "Proverb" },
  { text: "Be not afraid of going slowly, be afraid only of standing still.", author: "Chinese Proverb" },
  { text: "Drop by drop the water pot is filled.", author: "Dhammapada" },
  { text: "The sun will rise and we will try again.", author: "Proverb" },
  { text: "Quiet minds cannot be perplexed or frightened.", author: "Robert Louis Stevenson" },
  { text: "To know that you do not know is the best.", author: "Lao Tzu" },
  { text: "Never let the fear of striking out keep you from playing the game.", author: "Babe Ruth" },
  { text: "Silence is a source of great strength.", author: "Lao Tzu" },
  { text: "Energy and persistence conquer all things.", author: "Benjamin Franklin" },
  { text: "Knowledge is a treasure, but practice is the key to it.", author: "Thomas Fuller" },
  { text: "What we think, we become.", author: "Buddha" },
  { text: "Climb the mountain not to plant your flag, but to embrace the challenge.", author: "David McCullough Jr." },
  { text: "Begin at once to live, and count each separate day as a separate life.", author: "Seneca" },
  { text: "You must do the things you think you cannot do.", author: "Eleanor Roosevelt" },
  { text: "Wherever you go, go with all your heart.", author: "Confucius" },
  { text: "Live in the sunshine, swim the sea, drink the wild air.", author: "Ralph Waldo Emerson" },
  { text: "In three words I can sum up everything I've learned about life: it goes on.", author: "Robert Frost" },
  { text: "Every wall is a door.", author: "Ralph Waldo Emerson" },
  { text: "Act as if what you do makes a difference. It does.", author: "William James" },
  { text: "No act of kindness, no matter how small, is ever wasted.", author: "Aesop" },
  { text: "Look deep into nature, and then you will understand everything better.", author: "Albert Einstein" },
  { text: "Peace comes from within. Do not seek it without.", author: "Buddha" },
];

/**
 * Deterministically pick a quote for a given date string (YYYY-MM-DD),
 * ensuring the quote stays stable throughout the day and never flickers on refresh.
 */
export function getDailyQuote(dateStr?: string): QuoteItem {
  if (!dateStr) {
    const now = new Date();
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    const cst = new Date(utc + 3600000 * 8);
    dateStr = `${cst.getFullYear()}-${String(cst.getMonth() + 1).padStart(2, "0")}-${String(cst.getDate()).padStart(2, "0")}`;
  }

  // Hash string into integer
  let hash = 0;
  for (let i = 0; i < dateStr.length; i++) {
    hash = (hash << 5) - hash + dateStr.charCodeAt(i);
    hash |= 0;
  }
  const index = Math.abs(hash) % CURATED_QUOTES.length;
  return CURATED_QUOTES[index];
}

/**
 * Fetch random quote from Quotable API with short timeout, falling back to local list.
 */
export async function fetchQuoteWithFallback(dateStr?: string): Promise<QuoteItem> {
  const fallback = getDailyQuote(dateStr);
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1500);
    const res = await fetch("https://api.quotable.io/random?tags=inspirational|wisdom&maxLength=120", {
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    if (res.ok) {
      const data = await res.json();
      if (data?.content && data?.author) {
        return { text: data.content, author: data.author };
      }
    }
  } catch {
    // Graceful fallback to local dictionary
  }
  return fallback;
}
