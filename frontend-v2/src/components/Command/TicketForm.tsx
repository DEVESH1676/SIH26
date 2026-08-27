import React, { useState, useEffect } from "react";
import { Button } from "../ui/button";
import { z } from "zod";
import { motion, AnimatePresence } from "framer-motion";

interface TicketFormProps {
  onSubmit: (title: string, description: string) => void;
  isLoading: boolean;
}

const ticketSchema = z.object({
  title: z.string().min(3, "Subject must be at least 3 characters"),
  description: z.string().min(10, "Description must be at least 10 characters"),
});

type FormErrors = {
  title?: string;
  description?: string;
};

const TicketForm: React.FC<TicketFormProps> = ({ onSubmit, isLoading }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState({ title: false, description: false });

  useEffect(() => {
    const result = ticketSchema.safeParse({ title, description });
    if (!result.success) {
      const fieldErrors: FormErrors = {};
      result.error.issues.forEach((issue) => {
        if (issue.path[0] === "title") fieldErrors.title = issue.message;
        if (issue.path[0] === "description") fieldErrors.description = issue.message;
      });
      setErrors(fieldErrors);
    } else {
      setErrors({});
    }
  }, [title, description]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const result = ticketSchema.safeParse({ title, description });
    if (result.success) {
      onSubmit(title, description);
    }
  };

  const isValid = !errors.title && !errors.description && title.length > 0 && description.length > 0;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <div className="flex justify-between items-end ml-1">
          <label className="text-[10px] font-black text-zinc-100 uppercase tracking-widest">
            Subject
          </label>
          <AnimatePresence>
            {touched.title && errors.title && (
              <motion.span
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                className="text-[10px] font-bold text-red-400 uppercase tracking-tighter"
              >
                {errors.title}
              </motion.span>
            )}
          </AnimatePresence>
        </div>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onBlur={() => setTouched(prev => ({ ...prev, title: true }))}
          placeholder="e.g. VPN connection failing with error 619"
          disabled={isLoading}
          className={`w-full font-sans bg-black/20 border rounded-2xl px-5 py-4 text-sm text-white placeholder:text-zinc-500 focus:outline-none transition-all disabled:opacity-50 ${
            touched.title && errors.title 
              ? "border-red-500/50 focus:border-red-500 focus:ring-1 focus:ring-red-500/20" 
              : "border-white/10 focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20"
          }`}
        />
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-end ml-1">
          <label className="text-[10px] font-black text-zinc-100 uppercase tracking-widest">
            Description
          </label>
          <AnimatePresence>
            {touched.description && errors.description && (
              <motion.span
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                className="text-[10px] font-bold text-red-400 uppercase tracking-tighter"
              >
                {errors.description}
              </motion.span>
            )}
          </AnimatePresence>
        </div>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          onBlur={() => setTouched(prev => ({ ...prev, description: true }))}
          placeholder="Provide technical context, error codes, and affected systems..."
          disabled={isLoading}
          rows={6}
          className={`w-full font-sans bg-black/20 border rounded-2xl px-5 py-4 text-sm text-white placeholder:text-zinc-500 focus:outline-none transition-all resize-none disabled:opacity-50 ${
            touched.description && errors.description 
              ? "border-red-500/50 focus:border-red-500 focus:ring-1 focus:ring-red-500/20" 
              : "border-white/10 focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20"
          }`}
        />
      </div>

      <Button 
        type="submit" 
        disabled={isLoading || !isValid}
        className={`w-full font-sans h-16 rounded-2xl font-black uppercase tracking-[0.2em] text-[11px] transition-all duration-500 border ${
          isLoading || !isValid
            ? "bg-zinc-800 text-zinc-500 border-white/5 cursor-not-allowed opacity-50" 
            : "bg-white text-black border-cyan-400 hover:bg-cyan-400 hover:text-white hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_20px_rgba(34,211,238,0.4)]"
        }`}
      >
        {isLoading ? (
          <span className="flex items-center gap-3">
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            System Processing...
          </span>
        ) : (
          "Launch Intelligence Run"
        )}
      </Button>
    </form>
  );
};

export default TicketForm;
