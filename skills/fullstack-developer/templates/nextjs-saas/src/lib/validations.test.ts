import { describe, expect, it } from "vitest";
import { emailSchema, projectSchema } from "./validations";

describe("validations", () => {
  it("accepts a valid email", () => {
    expect(emailSchema.safeParse({ email: "a@b.co" }).success).toBe(true);
  });
  it("rejects an invalid email", () => {
    expect(emailSchema.safeParse({ email: "nope" }).success).toBe(false);
  });
  it("requires a project name", () => {
    expect(projectSchema.safeParse({ name: "  " }).success).toBe(false);
  });
});
