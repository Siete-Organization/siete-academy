import { forwardRef, type InputHTMLAttributes, type TextareaHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

const baseField =
  "flex w-full bg-transparent border-0 border-b border-bone-strong px-0 py-2.5 text-[15px] " +
  "placeholder:text-ink-faint focus-visible:outline-none focus-visible:border-ink transition-colors " +
  "disabled:opacity-50";

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input ref={ref} className={cn(baseField, "h-11", className)} {...props} />
  ),
);
Input.displayName = "Input";

export const Textarea = forwardRef<
  HTMLTextAreaElement,
  TextareaHTMLAttributes<HTMLTextAreaElement>
>(({ className, ...props }, ref) => (
  <textarea
    ref={ref}
    className={cn(baseField, "min-h-[140px] resize-y leading-relaxed", className)}
    {...props}
  />
));
Textarea.displayName = "Textarea";
