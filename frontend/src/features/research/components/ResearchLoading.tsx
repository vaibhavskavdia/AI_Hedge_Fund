import {
  Database,
  Brain,
  FileSearch,
  Sparkles,
  CheckCircle2,
} from "lucide-react";

interface Props {
  query: string;
}

const steps = [
  {
    icon: Database,
    title: "Searching Vector Database",
    description: "Finding relevant earnings calls and SEC filings.",
  },
  {
    icon: FileSearch,
    title: "Retrieving Context",
    description: "Selecting the most relevant financial documents.",
  },
  {
    icon: Brain,
    title: "Analyzing with AI",
    description: "Generating institutional-grade investment research.",
  },
  {
    icon: Sparkles,
    title: "Preparing Final Report",
    description: "Formatting insights for your review.",
  },
];

export default function ResearchLoading({
  query,
}: Props) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

      <div className="mb-8">

        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          AI Research
        </p>

        <h2 className="mt-2 text-3xl font-bold text-white">
          Generating Research Report
        </h2>

        <p className="mt-3 text-slate-400">
          "{query}"
        </p>

      </div>

      <div className="space-y-6">

        {steps.map((step, index) => {
          const Icon = step.icon;

          return (
            <div
              key={index}
              className="flex items-start gap-5 rounded-2xl border border-slate-800 bg-slate-950/40 p-5"
            >
              <div className="rounded-xl bg-blue-500/10 p-3">
                <Icon
                  size={22}
                  className="text-blue-400"
                />
              </div>

              <div className="flex-1">

                <div className="flex items-center justify-between">

                  <h3 className="font-semibold text-white">
                    {step.title}
                  </h3>

                  <CheckCircle2
                    size={18}
                    className="animate-pulse text-emerald-400"
                  />

                </div>

                <p className="mt-2 text-sm text-slate-400">
                  {step.description}
                </p>

              </div>
            </div>
          );
        })}

      </div>

      <div className="mt-10 h-2 overflow-hidden rounded-full bg-slate-800">
        <div className="h-full w-full animate-pulse rounded-full bg-blue-500" />
      </div>

    </div>
  );
}