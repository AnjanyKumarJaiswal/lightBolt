"use client";

import { Zap } from "lucide-react";
import TerminalPreview from "./components/terminal";

export default function Home() {
  return (
    <>
      <div className="flex flex-col justify-center items-center w-full h-screen bg-[url('/images/meshbg2.jpg')] bg-cover bg-center p-4 font-geistmono">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-card/50 backdrop-blur-sm border border-slate-900/90">
          <Zap className="w-4 h-4 text-black" />
          <span className="text-sm text-black">Lightning-fast Generation</span>
        </div>

        <div className="flex justify-center items-center p-4 max-w-[900px] h-[400px]">
          <div className="text-5xl md:text-6xl text-center font-semibold leading-tight text-black">
            The fastest way to generate backend-ready{" "}
            boiler<span className="text-zinc-300">plate</span> with{" "}
            <span className="text-zinc-300">Python</span>
          </div>
        </div>

        <div className="flex justify-center items-center mt-6 bg-black">
          <TerminalPreview />
        </div>
      </div>
    </>
  );
}
