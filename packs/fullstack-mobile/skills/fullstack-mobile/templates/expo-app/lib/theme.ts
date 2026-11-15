import { useColorScheme } from "react-native";

const palette = {
  light: { bg: "#ffffff", card: "#f1f5f9", text: "#0f172a", muted: "#64748b", primary: "#4f46e5", border: "#e2e8f0" },
  dark: { bg: "#020617", card: "#0f172a", text: "#f1f5f9", muted: "#94a3b8", primary: "#818cf8", border: "#1e293b" },
};

export function useTheme() {
  return palette[useColorScheme() === "dark" ? "dark" : "light"];
}
