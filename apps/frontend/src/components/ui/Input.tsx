import React from 'react';

export function Input({ className = '', ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input 
      className={`bg-background brutal-border p-3 w-full font-sans text-foreground focus:outline-none focus:border-accent transition-colors ${className}`}
      {...props}
    />
  );
}

export function TextArea({ className = '', ...props }: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea 
      className={`bg-background brutal-border p-3 w-full font-sans text-foreground focus:outline-none focus:border-accent transition-colors resize-y min-h-[120px] ${className}`}
      {...props}
    />
  );
}
