/**
 * Copyright 2026 Yug Dabgar
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { TextArea } from '@/components/ui/Input';
import { API_BASE_URL } from '@/lib/config';
import SettingsModal from '@/components/SettingsModal';

interface FailedModel {
  model: string;
  reason: string;
}

interface FallbackLogEntry {
  type: 'trying' | 'failed' | 'success';
  model: string;
  reason?: string;
  attempt?: number;
  total?: number;
}

interface ErrorState {
  message: string;
  provider_issue: boolean;
  failed_models: FailedModel[];
}

export default function AnalyzePage() {
  const [jobDesc, setJobDesc] = useState('');
  const [loading, setLoading] = useState(false);
  const [progressValue, setProgressValue] = useState(0);
  const [progressText, setProgressText] = useState('');
  const [fallbackLog, setFallbackLog] = useState<FallbackLogEntry[]>([]);
  const [errorState, setErrorState] = useState<ErrorState | null>(null);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const fallbackLogRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  useEffect(() => {
    const cvId = localStorage.getItem("indom_cv_id");
    if (!cvId) {
      router.push("/");
    }
  }, [router]);

  // Auto-scroll fallback log to bottom
  useEffect(() => {
    if (fallbackLogRef.current) {
      fallbackLogRef.current.scrollTop = fallbackLogRef.current.scrollHeight;
    }
  }, [fallbackLog]);

  const handleAnalyze = async () => {
    if (jobDesc.length < 100) {
      alert("Job description is too short (min 100 chars).");
      return;
    }

    setLoading(true);
    setProgressValue(0);
    setProgressText("Initializing AI Engine...");
    setFallbackLog([]);
    setErrorState(null);

    const cvId = localStorage.getItem("indom_cv_id");

    try {
      const res = await fetch(`${API_BASE_URL}/api/analyze/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cv_id: cvId, job_description: jobDesc }),
      });
      
      if (!res.ok) {
        throw new Error("Failed to start analysis stream. Is the backend running?");
      }
      
      const reader = res.body?.getReader();
      if (!reader) throw new Error("No stream reader available");
      
      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.replace('data: ', '').trim();
            if (!dataStr) continue;
            
            try {
              const data = JSON.parse(dataStr);
              
              // Handle provider-down error with structured data
              if (data.progress === -1 && data.provider_issue) {
                setErrorState({
                  message: data.status || "All AI models are currently unavailable",
                  provider_issue: true,
                  failed_models: data.failed_models || [],
                });
                setLoading(false);
                return;
              }
              
              // Handle regular error
              if (data.progress === -1) {
                const msg = data.status || "AI processing failed";
                if (msg.includes("NO_API_KEY") || msg.includes("NO_FALLBACK")) {
                  const cleanMsg = msg.replace("NO_API_KEY:", "").replace("NO_FALLBACK:", "");
                  setErrorState({
                    message: cleanMsg,
                    provider_issue: false,
                    failed_models: [],
                  });
                } else {
                  setErrorState({
                    message: msg,
                    provider_issue: false,
                    failed_models: [],
                  });
                }
                setLoading(false);
                return;
              }
              
              // Handle fallback events (progress -2 = failed model, don't update progress bar)
              if (data.fallback) {
                const fb = data.fallback as FallbackLogEntry;
                setFallbackLog(prev => [...prev, fb]);
              }
              
              // Update progress (skip -2 which is a fallback-failed signal)
              if (data.progress >= 0) {
                setProgressValue(data.progress);
              }
              setProgressText(data.status);
              
              if (data.result) {
                localStorage.setItem("indom_analysis", JSON.stringify(data.result));
                setTimeout(() => router.push("/dashboard"), 500);
              }
            } catch (parseErr) {
              // Re-throw actual errors, ignore JSON parse issues
              if (parseErr instanceof Error && parseErr.message !== "Unexpected end of JSON input") {
                throw parseErr;
              }
            }
          }
        }
      }
    } catch (err: any) {
      console.error(err);
      const msg = err.message || "Unknown error";
      setErrorState({
        message: msg,
        provider_issue: false,
        failed_models: [],
      });
      setLoading(false);
    }
  };

  // Render the error card
  const renderErrorCard = () => {
    if (!errorState) return null;

    return (
      <div className="w-full mt-2 animate-in fade-in">
        <div className="brutal-border brutal-shadow-warning bg-[#0a0a0a] p-6">
          {/* Header */}
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">⚠</span>
            <h3 className="text-lg font-heading uppercase text-[#ff3f3f]">
              {errorState.provider_issue ? "AI Models Unavailable" : "Configuration Error"}
            </h3>
          </div>

          {/* Description */}
          <p className="text-sm text-[#aaa] mb-4 leading-relaxed">
            {errorState.provider_issue
              ? "The AI providers are experiencing issues on their side. This is not an Indom bug."
              : errorState.message}
          </p>

          {/* Failed models list */}
          {errorState.provider_issue && errorState.failed_models.length > 0 && (
            <div className="mb-4 bg-[#111] brutal-border p-3">
              <p className="text-xs font-heading uppercase text-[#666] mb-2">Failed Models</p>
              <div className="flex flex-col gap-1.5">
                {errorState.failed_models.map((fm, i) => {
                  const modelShort = fm.model.split("/").pop() || fm.model;
                  return (
                    <div key={i} className="flex items-center justify-between text-xs font-mono">
                      <span className="text-[#ff3f3f]">✗ {modelShort}</span>
                      <span className="text-[#555]">{fm.reason}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* What you can do */}
          <div className="mb-5">
            <p className="text-xs font-heading uppercase text-[#666] mb-2">What you can do</p>
            <ul className="text-xs text-[#aaa] flex flex-col gap-1.5">
              <li>• Try a different model or provider in <span className="text-accent">⚙ Settings</span></li>
              <li>• Wait a few minutes and retry</li>
              {errorState.provider_issue && <li>• Check provider status pages for outage info</li>}
            </ul>
          </div>

          {/* Action buttons */}
          <div className="flex gap-3">
            <button
              onClick={() => setSettingsOpen(true)}
              className="flex-1 bg-[#111] brutal-border py-2.5 px-4 text-sm font-heading uppercase text-accent hover:bg-accent/10 transition-colors flex items-center justify-center gap-2"
            >
              <span>⚙</span> Open Settings
            </button>
            <button
              onClick={() => {
                setErrorState(null);
                handleAnalyze();
              }}
              className="flex-1 bg-accent text-background py-2.5 px-4 text-sm font-heading uppercase font-bold brutal-border border-accent hover:bg-accent/90 transition-colors flex items-center justify-center gap-2"
            >
              <span>↻</span> Retry
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <>
      <main className="flex flex-col items-center justify-center min-h-[70vh]">
        <Card className="w-full max-w-4xl">
          <h2 className="text-2xl mb-4 text-accent">Target Job Description</h2>
          <p className="mb-8 text-sm">
            Paste the entire job description below. Indom will use your AI model to cross-reference it with your CV, find the gaps, and dynamically tailor your skills to match.
          </p>

          <TextArea 
            placeholder="Paste Job Description here... (min 100 characters)" 
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            rows={12}
            className="mb-6"
            disabled={loading}
          />
          
          {/* Error state — styled card */}
          {errorState && !loading && renderErrorCard()}

          {/* Loading state — progress bar + live fallback log */}
          {loading && !errorState && (
            <div className="w-full mt-2 mb-2 flex flex-col items-center gap-6">
              <div className="bg-[#0a0a0a] rounded-xl p-2 border border-[#222] logo-pulse">
                <img src="/logo.png" alt="Indom" className="w-20 h-20 rounded-lg" />
              </div>
              <div className="w-full">
                <div className="flex justify-between mb-1">
                  <span className="text-xs font-bold text-accent uppercase">{progressText}</span>
                  <span className="text-xs font-bold text-accent">{progressValue > 0 ? `${progressValue}%` : ''}</span>
                </div>
                <div className="w-full bg-[#111] border-2 border-[#333] h-4 relative overflow-hidden">
                  <div 
                    className="bg-accent h-full transition-all duration-300"
                    style={{ width: `${Math.max(progressValue, 0)}%` }}
                  />
                </div>
              </div>

              {/* Live fallback log — only shows when fallback events start arriving */}
              {fallbackLog.length > 0 && (
                <div className="w-full bg-[#0a0a0a] brutal-border p-3 max-h-32 overflow-y-auto" ref={fallbackLogRef}>
                  <p className="text-[10px] font-heading uppercase text-[#444] mb-2">Model Fallback Log</p>
                  <div className="flex flex-col gap-1">
                    {fallbackLog.map((entry, i) => {
                      const modelShort = entry.model.split("/").pop() || entry.model;
                      if (entry.type === 'trying') {
                        return (
                          <div key={i} className="text-xs font-mono text-[#888]">
                            <span className="text-accent">⚡</span> Trying {modelShort}...
                          </div>
                        );
                      } else if (entry.type === 'failed') {
                        return (
                          <div key={i} className="text-xs font-mono text-[#ff3f3f]">
                            <span>✗</span> {modelShort} — {entry.reason || 'Failed'}
                          </div>
                        );
                      } else if (entry.type === 'success') {
                        return (
                          <div key={i} className="text-xs font-mono text-accent">
                            <span>✓</span> Connected to {modelShort}
                          </div>
                        );
                      }
                      return null;
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Default state — action buttons */}
          {!loading && !errorState && (
            <div className="flex justify-between items-center">
              <Button variant="ghost" onClick={() => router.push("/")}>Back</Button>
              <Button onClick={handleAnalyze} disabled={jobDesc.length < 100}>
                Commence Faking
              </Button>
            </div>
          )}
        </Card>
      </main>

      {/* Settings Modal — can be opened from error card */}
      <SettingsModal isOpen={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </>
  );
}
