# AI Features (Claude API)

Add chatbots, content generators, summarizers and document Q&A to any product.

## Rules
- Call the model **only from the server** (API route, server action, backend). Never ship the API key to the browser or mobile app.
- Env: `ANTHROPIC_API_KEY`. Choose the model in one config constant so it is easy to change (check https://docs.claude.com for current model names).
- Stream responses for chat UIs. Set `max_tokens`. Handle errors and rate limits (retry with backoff on 429/529).
- Rate-limit per user, cap input size, and log token usage per user/plan.
- Treat model output as untrusted: escape/sanitize before rendering HTML; never execute it.

## Install
```bash
npm i @anthropic-ai/sdk      # Node / Next.js
pip install anthropic        # Python
```

## Next.js streaming chat route
```ts
// src/app/api/chat/route.ts
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY
const MODEL = process.env.CLAUDE_MODEL ?? "claude-sonnet-5-5"; // keep in sync with docs.claude.com
const Body = z.object({
  messages: z.array(z.object({ role: z.enum(["user", "assistant"]), content: z.string().max(8000) })).max(40),
});

export async function POST(req: Request) {
  const parsed = Body.safeParse(await req.json());
  if (!parsed.success) return Response.json({ error: "Invalid request" }, { status: 400 });

  const stream = client.messages.stream({
    model: MODEL,
    max_tokens: 1024,
    system: "You are a helpful assistant for <Business>. Answer briefly. If unsure, say so.",
    messages: parsed.data.messages,
  });

  const encoder = new TextEncoder();
  return new Response(
    new ReadableStream({
      async start(controller) {
        try {
          for await (const event of stream) {
            if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
              controller.enqueue(encoder.encode(event.delta.text));
            }
          }
        } catch {
          controller.enqueue(encoder.encode("\n[Error: the assistant is unavailable, please try again.]"));
        } finally {
          controller.close();
        }
      },
    }),
    { headers: { "Content-Type": "text/plain; charset=utf-8" } },
  );
}
```
Client: `fetch("/api/chat", { method: "POST", body: JSON.stringify({ messages }) })`, then read `res.body.getReader()` and append chunks to the last assistant message.

## FastAPI
```python
from anthropic import Anthropic
client = Anthropic()

@app.post("/summarize")
def summarize(body: SummarizeIn, user: User = Depends(get_current_user)):
    msg = client.messages.create(
        model=settings.claude_model, max_tokens=600,
        messages=[{"role": "user", "content": f"Summarize in 5 bullet points:\n\n{body.text[:20000]}"}],
    )
    return {"summary": msg.content[0].text}
```

## Patterns
| Feature | How |
|---|---|
| Support chatbot | System prompt with business facts (hours, prices, policies) + chat history; hand off to WhatsApp/email when unsure |
| Content generator | Form → structured prompt (tone, length, language) → stream result → "copy" and "regenerate" buttons |
| Summarizer | Chunk long text, summarize each chunk, then summarize summaries |
| Document Q&A (RAG) | Split docs into chunks → embed with an embeddings provider → store in Postgres `pgvector` → retrieve top-k chunks → pass them to Claude with the question and ask it to cite sources |
| Structured extraction | Ask for JSON matching a schema (or use tool use with an `input_schema`), then validate with zod/pydantic |
| Agents / actions | Use tool use: define tools with JSON schemas, execute them server-side with auth checks, return results to the model |
| Multilingual | Tell the model to reply in the user's language; detect it from the latest message |

## Persisting chats
```
conversations(id, user_id, title, created_at)
messages(id, conversation_id, role, content, tokens_in, tokens_out, created_at)
```

## Checklist
- [ ] Key only on the server, model name in config
- [ ] Streaming + loading indicator + stop button
- [ ] Input validation, size limits, per-user rate limits
- [ ] Error message when the API fails
- [ ] Usage tracking per user/plan
