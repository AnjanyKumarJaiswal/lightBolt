"use client";

import { useState, useEffect } from "react";
import { Copy } from "lucide-react";

const TerminalPreview = () => {
  const [displayedCode, setDisplayedCode] = useState("");
  const [copied, setCopied] = useState(false);

  const codeLines = [
    "$ lightbolt <folder_name>",
    "--framework",
    "<framework_name>"
  ];

  useEffect(() => {
    let currentChar = 0;
    const fullText = codeLines.join(" ");
    const interval = setInterval(() => {
      if (currentChar < fullText.length) {
        setDisplayedCode(fullText.slice(0, currentChar + 1));
        currentChar++;
      } else {
        clearInterval(interval);
      }
    }, 30);

    return () => clearInterval(interval);
  }, []);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(displayedCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (err) {
      console.error("Failed to copy text:", err);
    }
  };

  return (
    <div
      className="terminal-window font-geistmono border border-zinc-500 rounded-lg max-w-8xl mx-auto animate-fade-in-up relative">
      <div className="flex items-center gap-2 px-4 py-3 bg-card/60 border-b border-border/30">
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-red-500/80" />
          <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
          <div className="w-3 h-3 rounded-full bg-green-500/80" />
        </div>
        <span className="font-normal text-s text-muted-foreground ml-2">
          Terminal
        </span>
        <Copy
          className="ml-auto cursor-pointer"
          onClick={handleCopy}
        />
      </div>
      <div className="p-6 text-sm leading-relaxed">
        <pre className="text-[hsl(var(--terminal-text))] whitespace-pre-wrap">
          {displayedCode}
          <span className="inline-block w-2 h-4 bg-[hsl(var(--terminal-text))] animate-pulse ml-1" />
        </pre>
      </div>

      {copied && (
        <div className="absolute top-[-3] right-4 text-xs text-zinc-100 font-medium">
          Copied!
        </div>
      )}
    </div>
  );
};

export default TerminalPreview;
