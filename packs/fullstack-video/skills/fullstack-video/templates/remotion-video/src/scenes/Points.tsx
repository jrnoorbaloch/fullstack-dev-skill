import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { PromoProps } from "../schema";

export const Points: React.FC<PromoProps> = ({ points, accent, background }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const scale = width / 1920;

  return (
    <AbsoluteFill style={{ background, justifyContent: "center", padding: 160 * scale, gap: 36 * scale }}>
      {points.map((point, i) => {
        const p = spring({ frame: frame - i * 18, fps, config: { damping: 200 } });
        const bar = interpolate(frame - i * 18, [0, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return (
          <div key={point} style={{ display: "flex", alignItems: "center", gap: 32 * scale, opacity: p, transform: `translateX(${(1 - p) * -80}px)` }}>
            <div style={{ width: 16 * scale, height: 90 * scale, borderRadius: 8, background: accent, transform: `scaleY(${bar})` }} />
            <span style={{ color: "white", fontSize: 88 * scale, fontWeight: 700, letterSpacing: "-0.02em" }}>{point}</span>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
