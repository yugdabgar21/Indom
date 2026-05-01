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

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { TextArea } from '@/components/ui/Input';
import { API_BASE_URL } from '@/lib/config';

export default function AnalyzePage() {
  const [jobDesc, setJobDesc] = useState('');
  const [loading, setLoading] = useState(false);
  const [progressValue, setProgressValue] = useState(0);
  const [progressText, setProgressText] = useState('');
  const router = useRouter();

  useEffect(() => {
    const cvId = localStorage.getItem("indom_cv_id");
    if (!cvId) {
      router.push("/");
    }
  }, [router]);

  const handleAnalyze = async () => {
    if (jobDesc.length < 100) {
      alert("Job description is too short (min 100 chars).");
      return;
    }

    setLoading(true);
    setProgressValue(0);
    setProgressText("Initializing AI Engine...");

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
              if (data.progress === -1) {
                throw new Error(data.status);
              }
              setProgressValue(data.progress);
              setProgressText(data.status);
              
              if (data.result) {
                localStorage.setItem("indom_analysis", JSON.stringify(data.result));
                setTimeout(() => router.push("/dashboard"), 500);
              }
            } catch (e) {
              if (e instanceof Error && e.message.startsWith("Error:")) {
                 throw e;
              }
            }
          }
        }
      }
    } catch (err: any) {
      console.error(err);
      alert(`AI Error: ${err.message}`);
      setLoading(false);
    }
  };

  return (
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
        
        {loading ? (
          <div className="w-full mt-2 mb-2 flex flex-col items-center gap-6">
            <div className="bg-[#0a0a0a] rounded-xl p-2 border border-[#222] logo-pulse">
              <img src="/logo.png" alt="Indom" className="w-20 h-20 rounded-lg" />
            </div>
            <div className="w-full">
              <div className="flex justify-between mb-1">
                <span className="text-xs font-bold text-accent uppercase">{progressText}</span>
                <span className="text-xs font-bold text-accent">{progressValue}%</span>
              </div>
              <div className="w-full bg-[#111] border-2 border-[#333] h-4 relative overflow-hidden">
                <div 
                  className="bg-accent h-full transition-all duration-300"
                  style={{ width: `${progressValue}%` }}
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="flex justify-between items-center">
            <Button variant="ghost" onClick={() => router.push("/")}>Back</Button>
            <Button onClick={handleAnalyze} disabled={jobDesc.length < 100}>
              Commence Faking
            </Button>
          </div>
        )}
      </Card>
    </main>
  );
}
