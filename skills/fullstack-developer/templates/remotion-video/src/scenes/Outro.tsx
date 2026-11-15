import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { PromoProps } from "../schema";

export const Outro: React.FC<PromoProps> = ({ cta, url, accent, background }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const scale = width / 1920;
  const pop = spring({ frame: frame - 5, fps, config: { damping: 12 } });
  const urlOpacity = interpolate(frame, [25, 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background, justifyContent: "center", alignItems: "center", gap: 40 * scale }}>
      <div
        style={{
          transform: `scale(${pop})`,
          background: accent,
          color: background,
          fontSize: 96 * scale,
          fontWeight: 800,
          padding: `${28 * scale}px ${72 * scale}px`,
          borderRadius: 999,
        }}
      >
        {cta}
      </div>
      <div style={{ opacity: urlOpacity, color: "rgba(255,255,255,0.75)", fontSize: 48 * scale }}>{url}</div>
    </AbsoluteFill>
  );
};
