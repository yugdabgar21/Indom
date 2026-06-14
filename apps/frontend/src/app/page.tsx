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

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { API_BASE_URL } from '@/lib/config';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE_URL}/api/cv/upload`, {
        method: "POST",
        body: formData,
      });
      
      if (!res.ok) throw new Error("Failed to upload CV");
      const data = await res.json();
      
      localStorage.setItem("indom_cv_id", data.cv_id);
      
      router.push("/analyze");
    } catch (err) {
      console.error(err);
      alert("Failed to upload CV. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-[70vh]">
      <Card className="w-full max-w-xl">
        <h2 className="text-2xl mb-4 text-accent">Upload Master CV</h2>
        <p className="mb-8 text-sm">
          Upload your text-based PDF CV. We will extract the text and save it locally.
          Image-based CVs are not supported in the MVP.
        </p>
        
        <div className="flex flex-col gap-6">
          <label className="flex flex-col items-center justify-center w-full h-32 brutal-border border-dashed cursor-pointer hover:bg-white/5 transition-colors">
            <span className="font-heading uppercase text-sm">
              {file ? file.name : "Click to select PDF"}
            </span>
            <input 
              type="file" 
              accept=".pdf" 
              className="hidden" 
              onChange={handleFileChange} 
            />
          </label>
          
          <Button 
            onClick={handleUpload} 
            disabled={!file || loading}
            fullWidth
          >
            {loading ? "Parsing..." : "Upload & Continue"}
          </Button>
        </div>
      </Card>
    </main>
  );
}
