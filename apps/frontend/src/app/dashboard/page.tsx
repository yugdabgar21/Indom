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

export default function DashboardPage() {
  const [analysis, setAnalysis] = useState<any>(null);
  const [latexCode, setLatexCode] = useState('');
  const [pdfUrl, setPdfUrl] = useState('');
  const [tab, setTab] = useState<'code' | 'preview'>('preview');
  const [loadingPdf, setLoadingPdf] = useState(false);
  const [copied, setCopied] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const [checkedSkills, setCheckedSkills] = useState<Record<number, boolean>>({});
  const router = useRouter();

  useEffect(() => {
    const dataStr = localStorage.getItem("indom_analysis");
    if (!dataStr) {
      router.push("/");
      return;
    }
    const data = JSON.parse(dataStr);
    setAnalysis(data);
    generateInitialLatex(data);
  }, [router]);

  const generateInitialLatex = async (analysisData: any) => {
    const cvId = localStorage.getItem("indom_cv_id");
    try {
      const res = await fetch("http://localhost:8000/api/generate/latex", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cv_id: cvId, analysis: analysisData, template_name: "classic.tex" }),
      });
      const data = await res.json();
      setLatexCode(data.latex_code);
      compilePdf(data.latex_code, analysisData);
    } catch (err) {
      console.error(err);
    }
  };

  const [pdfProgress, setPdfProgress] = useState(0);
  const [pdfStatus, setPdfStatus] = useState('');

  const compilePdf = async (code: string, analysisData?: any) => {
    setLoadingPdf(true);
    setPdfProgress(0);
    setPdfStatus('Starting compilation...');
    const cvId = localStorage.getItem("indom_cv_id");
    const analysisToUse = analysisData || analysis;
    try {
      const res = await fetch(`${API_BASE_URL}/api/compile/pdf/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cv_id: cvId, analysis: analysisToUse, template_name: "classic.tex" }),
      });

      if (!res.ok) {
        throw new Error("Compile stream failed");
      }

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();
      if (!reader) throw new Error("No stream reader");

      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const payload = JSON.parse(line.slice(6));
              if (payload.progress === -1) {
                throw new Error(payload.status);
              }
              setPdfProgress(payload.progress);
              setPdfStatus(payload.status);
              if (payload.progress === 100 && payload.pdf_base64) {
                const binaryStr = atob(payload.pdf_base64);
                const bytes = new Uint8Array(binaryStr.length);
                for (let i = 0; i < binaryStr.length; i++) {
                  bytes[i] = binaryStr.charCodeAt(i);
                }
                const blob = new Blob([bytes], { type: 'application/pdf' });
                const url = URL.createObjectURL(blob);
                setPdfUrl(url);
              }
            } catch (parseErr: any) {
              if (parseErr.message?.startsWith('Error:')) throw parseErr;
            }
          }
        }
      }
    } catch (err: any) {
      console.error(err);
      alert("Failed to compile PDF: " + err.message);
    } finally {
      setLoadingPdf(false);
      setPdfProgress(0);
      setPdfStatus('');
    }
  };

  const handleDownload = () => {
    if (!pdfUrl) return;
    const name = (analysis?.full_name || 'CV').replace(/[^a-zA-Z0-9 ]/g, '').replace(/\s+/g, '_');
    const title = (analysis?.job_title || 'Tailored').replace(/[^a-zA-Z0-9 ]/g, '').replace(/\s+/g, '_');
    const filename = `${name}_${title}_Indom.pdf`;
    const a = document.createElement("a");
    a.href = pdfUrl;
    a.download = filename;
    a.click();
    setDownloaded(true);
  };

  const handleStartOver = () => {
    localStorage.removeItem("indom_analysis");
    router.push("/analyze");
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(latexCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!analysis) return <div className="p-8 text-accent animate-pulse font-heading">Loading Indom Core...</div>;

  return (
    <main className="grid grid-cols-1 lg:grid-cols-3 gap-8 min-h-[85vh]">
      
      {/* LEFT PANEL - CV OUTPUT */}
      <div className="lg:col-span-2 flex flex-col h-full">
        <div className="flex justify-between items-center mb-4">
          <div className="flex gap-2">
            <Button 
              variant={tab === 'preview' ? 'primary' : 'ghost'} 
              onClick={() => setTab('preview')}
              className="py-2 px-4 text-sm"
            >
              PDF Preview
            </Button>
            <Button 
              variant={tab === 'code' ? 'primary' : 'ghost'} 
              onClick={() => setTab('code')}
              className="py-2 px-4 text-sm"
            >
              LaTeX Code
            </Button>
          </div>
          <div className="flex gap-2">
            {tab === 'code' && (
              <Button variant="ghost" onClick={handleCopyCode} className="py-2 px-4 text-sm border-foreground">
                {copied ? "Copied!" : "Copy Code"}
              </Button>
            )}
            <Button variant="primary" onClick={handleDownload} disabled={!pdfUrl} className="py-2 px-4 text-sm">
              {downloaded ? '✓ Downloaded' : 'Download PDF'}
            </Button>
            <Button variant="ghost" onClick={handleStartOver} className="py-2 px-4 text-sm border-foreground">
              Start Over
            </Button>
          </div>
        </div>

        {downloaded && (
          <div className="text-center py-2 text-accent font-heading text-sm animate-pulse">
            CV ready. Now go get in the room. 🔥
          </div>
        )}

        <Card className="flex-grow flex flex-col p-0 overflow-hidden h-[700px]">
          {tab === 'code' ? (
            <TextArea 
              value={latexCode} 
              onChange={(e) => setLatexCode(e.target.value)}
              className="w-full h-full p-4 font-mono text-sm border-none bg-[#111]"
            />
          ) : (
            <div className="w-full h-full bg-[#111] flex items-center justify-center">
              {loadingPdf ? (
                <div className="flex flex-col items-center gap-4 w-3/4 max-w-md">
                  <div className="bg-[#0a0a0a] rounded-lg p-1 border border-[#222] logo-pulse">
                    <img src="/logo.png" alt="Indom" className="w-16 h-16 rounded-md" />
                  </div>
                  <div className="text-accent font-heading text-lg">{pdfStatus || 'Compiling...'}</div>
                  <div className="w-full h-3 bg-[#222] border border-[#333] rounded-none overflow-hidden">
                    <div 
                      className="h-full bg-accent transition-all duration-300 ease-out"
                      style={{ width: `${pdfProgress}%` }}
                    />
                  </div>
                  <div className="text-[#888] text-sm font-mono">{pdfProgress}%</div>
                </div>
              ) : pdfUrl ? (
                <iframe src={pdfUrl} className="w-full h-full border-none" title="PDF Preview" />
              ) : (
                <div className="text-warning font-heading">No PDF Generated</div>
              )}
            </div>
          )}
        </Card>
      </div>

      {/* RIGHT PANEL - WARNING & ROADMAP */}
      <div className="flex flex-col gap-6">
        <Card className="border-warning border-2">
          <h3 className="text-warning font-heading font-bold uppercase text-lg mb-2">Faking Warning</h3>
          <p className="text-sm mb-4">The AI added the following skills to match the job description. Do not apply unless you plan to learn these before the interview.</p>
          <ul className="list-none pl-0 text-warning text-sm font-bold flex flex-col gap-2">
            {analysis.faked_skills?.map((skill: string, i: number) => (
              <li key={i} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={checkedSkills[i] || false}
                  onChange={() => setCheckedSkills(prev => ({ ...prev, [i]: !prev[i] }))}
                  className="accent-accent w-4 h-4 cursor-pointer"
                />
                <span className={checkedSkills[i] ? 'line-through opacity-50' : ''}>{skill}</span>
              </li>
            ))}
            {(!analysis.faked_skills || analysis.faked_skills.length === 0) && (
              <li>No skills faked. Pure 100% match.</li>
            )}
          </ul>
        </Card>

        <Card>
          <h3 className="text-accent font-heading font-bold uppercase text-lg mb-2">Match Score</h3>
          <div className="flex justify-between text-sm items-center">
            <span className="text-[#888]">Original CV:</span>
            <span className="font-bold">{analysis.match_score_before}%</span>
          </div>
          <div className="flex justify-between text-sm items-center mt-2 border-t border-[#333] pt-2">
            <span className="text-[#888]">Tailored CV:</span>
            <span className="text-accent font-bold text-2xl">{analysis.match_score_after}%</span>
          </div>
        </Card>

        <Card className="flex-grow overflow-y-auto max-h-[400px]">
          <h3 className="text-foreground font-heading font-bold uppercase text-lg mb-4">5-Day Roadmap</h3>
          <div className="flex flex-col gap-4">
            {analysis.roadmap?.days?.map((day: any) => (
              <div key={day.day} className="brutal-border p-3 border-[#333]">
                <div className="font-bold text-accent text-sm uppercase mb-1">Day {day.day}: {day.topic}</div>
                <p className="text-xs text-[#888] mb-2">{day.description}</p>
                <div className="flex flex-col gap-1">
                  {day.resources?.map((res: any, idx: number) => (
                    <a 
                      key={idx} 
                      href={res.url} 
                      target="_blank" 
                      rel="noreferrer"
                      className="text-xs text-[#00aaff] hover:underline truncate block"
                    >
                      ▶ {res.title}
                    </a>
                  ))}
                  {(!day.resources || day.resources.length === 0) && (
                    <span className="text-xs text-[#555]">No verified links fetched.</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </main>
  );
}
