import { useEffect, useState } from "react";
import { FlatList, KeyboardAvoidingView, Platform, Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { loadJSON, saveJSON } from "@/lib/storage";
import { useTheme } from "@/lib/theme";

type Item = { id: string; title: string; done: boolean };
const KEY = "items";

export default function Home() {
  const t = useTheme();
  const [items, setItems] = useState<Item[]>([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadJSON<Item[]>(KEY, []).then((data) => { setItems(data); setLoading(false); });
  }, []);

  function update(next: Item[]) {
    setItems(next);
    saveJSON(KEY, next);
  }

  function add() {
    const title = text.trim();
    if (!title) return;
    update([{ id: Date.now().toString(), title, done: false }, ...items]);
    setText("");
  }

  return (
    <SafeAreaView edges={["bottom"]} style={[styles.screen, { backgroundColor: t.bg }]}>
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={{ flex: 1 }}>
        <View style={styles.row}>
          <TextInput
            value={text}
            onChangeText={setText}
            onSubmitEditing={add}
            placeholder="Add an item"
            placeholderTextColor={t.muted}
            accessibilityLabel="New item"
            style={[styles.input, { color: t.text, borderColor: t.border }]}
          />
          <Pressable onPress={add} accessibilityRole="button" style={[styles.button, { backgroundColor: t.primary }]}>
            <Text style={styles.buttonText}>Add</Text>
          </Pressable>
        </View>
        {loading ? (
          <Text style={[styles.empty, { color: t.muted }]}>Loading…</Text>
        ) : (
          <FlatList
            data={items}
            keyExtractor={(i) => i.id}
            ListEmptyComponent={<Text style={[styles.empty, { color: t.muted }]}>Nothing here yet. Add your first item.</Text>}
            renderItem={({ item }) => (
              <Pressable
                onPress={() => update(items.map((i) => (i.id === item.id ? { ...i, done: !i.done } : i)))}
                onLongPress={() => update(items.filter((i) => i.id !== item.id))}
                style={[styles.card, { backgroundColor: t.card }]}
              >
                <Text style={{ color: t.text, textDecorationLine: item.done ? "line-through" : "none" }}>{item.title}</Text>
              </Pressable>
            )}
          />
        )}
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, padding: 16 },
  row: { flexDirection: "row", gap: 8, marginBottom: 16 },
  input: { flex: 1, borderWidth: 1, borderRadius: 10, paddingHorizontal: 12, minHeight: 44 },
  button: { borderRadius: 10, paddingHorizontal: 16, justifyContent: "center", minHeight: 44 },
  buttonText: { color: "#fff", fontWeight: "600" },
  card: { padding: 16, borderRadius: 12, marginBottom: 8 },
  empty: { textAlign: "center", marginTop: 40 },
});
