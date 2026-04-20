import { type ButtonHTMLAttributes, forwardRef } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 font-medium transition-all duration-200 disabled:opacity-40 disabled:pointer-events-none select-none",
  {
    variants: {
      variant: {
        default:
          "bg-ink text-paper hover:bg-ink-soft rounded-md shadow-frame [&>svg]:transition-transform hover:[&>svg]:translate-x-0.5",
        outline:
          "border border-ink/70 text-ink hover:border-ink hover:bg-ink hover:text-paper rounded-md",
        ghost: "text-ink hover:bg-bone/60 rounded-md",
        subtle: "bg-bone/60 text-ink hover:bg-bone rounded-md",
        ember:
          "bg-ember text-paper hover:bg-ember/90 rounded-md shadow-frame [&>svg]:transition-transform hover:[&>svg]:translate-x-0.5",
        link: "text-ink underline-offset-4 decoration-ink/30 hover:decoration-ink px-0 h-auto underline",
        destructive: "bg-ember/90 text-paper hover:bg-ember rounded-md",
      },
      size: {
        default: "h-11 px-5 text-sm tracking-tight",
        sm: "h-9 px-3.5 text-xs",
        lg: "h-12 px-7 text-[15px]",
        icon: "h-10 w-10 rounded-md",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button ref={ref} className={cn(buttonVariants({ variant, size }), className)} {...props} />
  ),
);
Button.displayName = "Button";
