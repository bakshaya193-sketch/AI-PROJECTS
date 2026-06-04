const EMOJI = { positive: "😊", neutral: "😐", negative: "😔" };
const COLOR = { positive: "#10b981", neutral: "#6b7280", negative: "#ef4444" };

export default function SentimentBadge({ sentiment, score }) {
  if (!sentiment) return null;
  return (
    <span
      className="sentiment-badge"
      style={{ color: COLOR[sentiment] }}
      title={`Sentiment: ${sentiment} (score: ${score?.toFixed(2)})`}
    >
      {EMOJI[sentiment]}
    </span>
  );
}
