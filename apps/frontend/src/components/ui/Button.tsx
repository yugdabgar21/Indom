import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'warning' | 'ghost';
  fullWidth?: boolean;
}

export function Button({ children, variant = 'primary', fullWidth, className = '', ...props }: ButtonProps) {
  const baseStyles = "px-6 py-3 font-heading font-bold uppercase transition-all duration-200 brutal-border disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer";
  
  const variants = {
    primary: "bg-accent text-background brutal-shadow-hover hover:bg-[#00e676]",
    warning: "bg-warning text-foreground brutal-shadow-warning hover:bg-[#e63939]",
    ghost: "bg-transparent text-foreground hover:bg-white/10"
  };

  const width = fullWidth ? "w-full" : "";

  return (
    <button 
      className={`${baseStyles} ${variants[variant]} ${width} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
