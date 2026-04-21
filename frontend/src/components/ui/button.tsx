import { type ButtonHTMLAttributes, forwardRef } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

// Rebrand 2026: pill-shaped buttons (border-radius: 33px) matcheando wearesiete.com.
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 font-semibold transition-all duration-200 disabled:opacity-40 disabled:pointer-events-none select-none rounded-full",
  {
    variants: {
      variant: {
        default:
          "bg-ink text-paper hover:bg-ink-soft [&>svg]:transition-transform hover:[&>svg]:translate-x-0.5",
        outline:
          "border border-ink/70 text-ink hover:border-ink hover:bg-ink hover:text-paper",
        ghost: "text-ink hover:bg-bone/60",
        subtle: "bg-bone/60 text-ink hover:bg-bone",
        ember:
          "bg-ember text-paper hover:bg-ember-soft [&>svg]:transition-transform hover:[&>svg]:translate-x-0.5",
        link: "text-ember underline-offset-4 decoration-ember/40 hover:decoration-ember px-0 h-auto underline rounded-none",
        destructive: "bg-ember text-paper hover:bg-ember-soft",
      },
      size: {
        default: "h-11 px-6 text-sm tracking-tight",
        sm: "h-9 px-4 text-xs",
        lg: "h-12 px-7 text-[15px]",
        icon: "h-10 w-10 rounded-full",
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
