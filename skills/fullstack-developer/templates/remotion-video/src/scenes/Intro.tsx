import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { PromoProps } from "../schema";

export const Intro: React.FC<PromoProps> = ({ brand, headline, accent, background }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const scale = width / 1920;
  const pop = spring({ frame, fps, config: { damping: 14 } });
  const words = headline.split(" ");

  return (
    <AbsoluteFill style={{ background, justifyContent: "center", alignItems: "center", gap: 40 * scale, padding: 80 * scale }}>
      <div
        style={{
          transform: `scale(${pop})`,
          color: accent,
          fontSize: 44 * scale,
          fontWeight: 700,
          letterSpacing: "0.2em",
          textTransform: "uppercase",
        }}
      >
        {brand}
      </div>
      <h1 style={{ margin: 0, color: "white", fontSize: 140 * scale, lineHeight: 1.05, textAlign: "center", letterSpacing: "-0.03em" }}>
        {words.map((w, i) => {
          const p = spring({ frame: frame - 10 - i * 4, fps, config: { damping: 200 } });
          return (
            <span key={i} style={{ display: "inline-block", marginRight: "0.25em", opacity: p, transform: `translateY(${interpolate(p, [0, 1], [60, 0])}px)` }}>
              {w}
            </span>
          );
        })}
      </h1>
    </AbsoluteFill>
  );
};
