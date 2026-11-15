import { z } from "zod";

export const emailSchema = z.object({ email: z.string().trim().email("Enter a valid email address") });

export const projectSchema = z.object({
  name: z.string().trim().min(1, "Name is required").max(100, "Name is too long"),
});
