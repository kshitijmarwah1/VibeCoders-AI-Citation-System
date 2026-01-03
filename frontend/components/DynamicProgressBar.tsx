"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2, CheckCircle2, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

interface ProgressData {
  completed: number;
  total: number;
  current: string;
  status: "pending" | "processing" | "completed" | "error";
  percentage: number;
}

interface DynamicProgressBarProps {
  taskId: string | null;
  onComplete?: () => void;
}

export function DynamicProgressBar({ taskId, onComplete }: DynamicProgressBarProps) {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [showFireworks, setShowFireworks] = useState(false);

  useEffect(() => {
    if (!taskId) {
      setProgress(null);
      setShowFireworks(false);
      return;
    }

    // Poll for progress updates
    const pollProgress = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/progress/${taskId}`);
        if (response.ok) {
          const data = await response.json();
          setProgress(data);

          if (data.status === "completed") {
            setShowFireworks(true);
            setTimeout(() => {
              setShowFireworks(false);
              if (onComplete) onComplete();
            }, 2500);
            return; // Stop polling
          }

          if (data.status === "error") {
            setTimeout(() => {
              if (onComplete) onComplete();
            }, 1000);
            return; // Stop polling
          }
        }
      } catch (error) {
        console.error("Progress polling error:", error);
      }
    };

    // Initial poll
    pollProgress();

    // Poll every 200ms for smooth updates
    const interval = setInterval(pollProgress, 200);

    return () => clearInterval(interval);
  }, [taskId, onComplete]);

  if (!progress || !taskId) {
    return null;
  }

  return (
    <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm relative overflow-hidden">
      <CardContent className="p-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {progress.status === "processing" && (
                <Loader2 className="h-5 w-5 text-cyan-400 animate-spin" />
              )}
              {progress.status === "completed" && (
                <CheckCircle2 className="h-5 w-5 text-green-400" />
              )}
              <span className="text-white font-medium">{progress.current || "Processing..."}</span>
            </div>
            <span className="text-cyan-400 font-semibold text-lg">
              {Math.round(progress.percentage)}%
            </span>
          </div>

          {/* Animated Progress Bar */}
          <div className="relative w-full bg-black/60 rounded-full h-3 overflow-hidden">
            <div
              className={cn(
                "h-full transition-all duration-300 ease-out relative",
                showFireworks
                  ? "bg-gradient-to-r from-green-400 via-cyan-400 to-pink-500"
                  : "bg-gradient-to-r from-cyan-400 via-pink-500 to-purple-500"
              )}
              style={{ width: `${progress.percentage}%` }}
            >
              {/* Shimmer effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer" />
            </div>
          </div>

          {progress.total > 0 && (
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>Progress: {progress.completed} / {progress.total}</span>
              <span className={cn(
                "px-2 py-1 rounded-full",
                progress.status === "processing" && "bg-cyan-500/20 text-cyan-400",
                progress.status === "completed" && "bg-green-500/20 text-green-400",
                progress.status === "error" && "bg-red-500/20 text-red-400"
              )}>
                {progress.status}
              </span>
            </div>
          )}

          {/* Firework Animation */}
          {showFireworks && (
            <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-lg">
              {[...Array(30)].map((_, i) => {
                const angle = (i * 360) / 30;
                const distance = 80 + (i % 3) * 20;
                return (
                  <div
                    key={i}
                    className="absolute top-1/2 left-1/2 animate-firework"
                    style={{
                      '--delay': `${i * 0.05}s`,
                      '--angle': `${angle}deg`,
                      '--distance': `${distance}px`,
                    } as React.CSSProperties & { '--distance': string }}
                  >
                    <Sparkles className="h-3 w-3 text-yellow-400" />
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

