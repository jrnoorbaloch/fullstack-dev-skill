import { z } from "zod";
import { zColor } from "@remotion/zod-types";

export const promoSchema = z.object({
  brand: z.string(),
  headline: z.string(),
  points: z.array(z.string()).max(4),
  cta: z.string(),
  url: z.string(),
  accent: zColor(),
  background: zColor(),
});

export type PromoProps = z.infer<typeof promoSchema>;

export const defaultPromo: PromoProps = {
  brand: "{{BRAND}}",
  headline: "Build faster. Ship sooner.",
  points: ["Plan in minutes", "Build with confidence", "Launch anywhere"],
  cta: "Try it free",
  url: "example.com",
  accent: "#7c8cff",
  background: "#0b1020",
};
