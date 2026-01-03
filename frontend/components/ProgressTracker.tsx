"use client";

import { useEffect, useState } from "react";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface ProgressData {
  completed: number;
  total: number;
  current: string;
  status: "pending" | "processing" | "completed" | "error";
  percentage: number;
}

interface ProgressTrackerProps {
  taskId?: string;
  onComplete?: () => void;
}

export function ProgressTracker({ taskId, onComplete }: ProgressTrackerProps) {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (!taskId) {
      setIsVisible(false);
      return;
    }

    setIsVisible(true);
    const eventSource = new EventSource(`http://127.0.0.1:8000/progress/stream/${taskId}`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setProgress(data);

        if (data.status === "completed" || data.status === "error") {
          eventSource.close();
          if (onComplete) {
            setTimeout(onComplete, 1000);
          }
        }
      } catch (e) {
        console.error("Failed to parse progress data:", e);
      }
    };

    eventSource.onerror = () => {
      eventSource.close();
      setIsVisible(false);
    };

    return () => {
      eventSource.close();
    };
  }, [taskId, onComplete]);

  if (!isVisible || !progress) {
    return null;
  }

  return (
    <Card className="border-cyan-500/30 bg-black/40 backdrop-blur-sm">
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
              {progress.status === "error" && (
                <AlertCircle className="h-5 w-5 text-red-400" />
              )}
              <span className="text-white font-medium">
                {progress.status === "processing" && "Processing..."}
                {progress.status === "completed" && "Complete!"}
                {progress.status === "error" && "Error"}
              </span>
            </div>
            <span className="text-cyan-400 font-semibold">
              {Math.round(progress.percentage)}%
            </span>
          </div>

          <Progress value={progress.percentage} className="h-2" />

          {progress.current && (
            <p className="text-sm text-gray-400 truncate">
              {progress.current}
            </p>
          )}

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
        </div>
      </CardContent>
    </Card>
  );
}

