import Constants from "expo-constants";
import { StyleSheet, Text, View } from "react-native";
import { useTheme } from "@/lib/theme";

export default function Settings() {
  const t = useTheme();
  return (
    <View style={[styles.screen, { backgroundColor: t.bg }]}>
      <Text style={[styles.title, { color: t.text }]}>Settings</Text>
      <Text style={{ color: t.muted }}>Version {Constants.expoConfig?.version ?? "1.0.0"}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, padding: 16, gap: 8 },
  title: { fontSize: 22, fontWeight: "700" },
});
