import { AbsoluteFill } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { Intro } from "./scenes/Intro";
import { Points } from "./scenes/Points";
import { Outro } from "./scenes/Outro";
import type { PromoProps } from "./schema";

const INTRO = 75;
const POINTS = 120;
const OUTRO = 90;
const T = 15; // transition length (frames)
export const PROMO_DURATION = INTRO + POINTS + OUTRO - 2 * T;

export const Promo: React.FC<PromoProps> = (props) => (
  <AbsoluteFill style={{ backgroundColor: props.background, fontFamily: "Inter, system-ui, sans-serif" }}>
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={INTRO}>
        <Intro {...props} />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={slide({ direction: "from-right" })} timing={linearTiming({ durationInFrames: T })} />
      <TransitionSeries.Sequence durationInFrames={POINTS}>
        <Points {...props} />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: T })} />
      <TransitionSeries.Sequence durationInFrames={OUTRO}>
        <Outro {...props} />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  </AbsoluteFill>
);
