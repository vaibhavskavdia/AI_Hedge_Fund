interface Props {
  onSelect: (query: string) => void;
}

const queries = [
  "What did Tesla management say about AI?",
  "Summarize Nvidia's latest earnings call.",
  "How is Amazon AWS performing?",
  "What are Apple's biggest risks?",
  "What is Microsoft's AI strategy?",
  "Healthcare sector outlook for 2026",
  "Banking sector credit risks",
  "Top opportunities in semiconductor industry",
];

export default function SuggestedQueries({
  onSelect,
}: Props) {
  return (
    <div>

      <div className="mb-5">
        <p className="text-xs uppercase tracking-[0.35em] text-slate-500">
          Popular Research Questions
        </p>
      </div>

      <div className="flex flex-wrap gap-4">

        {queries.map((query) => (
          <button
            key={query}
            onClick={() => onSelect(query)}
            className="
                rounded-full
                border
                border-slate-700
                bg-slate-900
                px-5
                py-3
                text-sm
                text-slate-300
                transition
                hover:border-blue-500
                hover:bg-blue-500/10
                hover:text-white
            "
          >
            {query}
          </button>
        ))}

      </div>

    </div>
  );
}