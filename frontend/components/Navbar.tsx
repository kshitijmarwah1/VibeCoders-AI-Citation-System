"use client";

import { Brain, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-cyan-500/20 bg-black/80 backdrop-blur-xl">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <div className="relative">
              <Brain className="h-8 w-8 text-cyan-400 animate-pulse" />
              <Sparkles className="h-4 w-4 text-pink-500 absolute -top-1 -right-1 animate-spin" />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-400 via-pink-500 to-purple-500 bg-clip-text text-transparent">
                VibeVerifier
              </h1>
              <p className="text-xs text-gray-400">AI Hallucination Detector</p>
            </div>
          </Link>
          
          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2 text-sm text-gray-400">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
              <span>System Online</span>
            </div>
            <Link href="/docs">
              <Button variant="ghost" size="sm" className="text-cyan-400 hover:text-cyan-300">
                Docs
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

