import { Composition } from "remotion";
import { Promo, PROMO_DURATION } from "./Promo";
import { defaultPromo, promoSchema } from "./schema";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Promo"
      component={Promo}
      durationInFrames={PROMO_DURATION}
      fps={30}
      width={1920}
      height={1080}
      schema={promoSchema}
      defaultProps={defaultPromo}
    />
    <Composition
      id="PromoVertical"
      component={Promo}
      durationInFrames={PROMO_DURATION}
      fps={30}
      width={1080}
      height={1920}
      schema={promoSchema}
      defaultProps={defaultPromo}
    />
  </>
);
