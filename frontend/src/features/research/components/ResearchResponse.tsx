import { FileText, Copy, Check } from "lucide-react";
import { useState } from "react";

interface Props {
  response: string;
}

export default function ResearchResponse({
  response,
}: Props) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    await navigator.clipboard.writeText(response);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  return (
    <section className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

      <div className="mb-8 flex items-center justify-between">

        <div>

          <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
            AI Generated Report
          </p>

          <h2 className="mt-2 text-3xl font-bold text-white">
            Institutional Research
          </h2>

        </div>

        <button
          onClick={copy}
          className="flex items-center gap-2 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-300 transition hover:border-blue-500"
        >
          {copied ? (
            <>
              <Check
                size={18}
                className="text-green-400"
              />
              Copied
            </>
          ) : (
            <>
              <Copy size={18} />
              Copy
            </>
          )}
        </button>

      </div>

      <div className="rounded-2xl border border-slate-800 bg-slate-950/40 p-8">

        <div className="mb-6 flex items-center gap-3">

          <FileText
            size={22}
            className="text-blue-400"
          />

          <h3 className="text-xl font-semibold text-white">
            Analyst Report
          </h3>

        </div>

        <div className="whitespace-pre-wrap leading-8 text-slate-300">
          {response}
        </div>

      </div>

    </section>
  );
}