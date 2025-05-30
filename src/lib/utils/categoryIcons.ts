import { 
  SiHtml5, 
  SiCss3, 
  SiRuby, 
  SiRubyonrails, 
  SiJavascript, 
  SiPython, 
  SiLinux,
  SiGit 
} from 'react-icons/si';
import { 
  Database, 
  Globe, 
  Code, 
  Terminal, 
  Cpu,
  Settings,
  Book
} from 'lucide-react';
import { Category } from '../api/types';

interface CategoryIconConfig {
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  bgColor: string;
}

// カテゴリースラッグに対応するアイコン設定
const categoryIconMap: Record<string, CategoryIconConfig> = {
  'html-css': {
    icon: SiHtml5,
    color: 'text-orange-500',
    bgColor: 'bg-orange-50',
  },
  'ruby': {
    icon: SiRuby,
    color: 'text-red-700',
    bgColor: 'bg-red-100',
  },
  'ruby-rails': {
    icon: SiRubyonrails,
    color: 'text-rose-600',
    bgColor: 'bg-rose-100',
  },
  'javascript': {
    icon: SiJavascript,
    color: 'text-amber-500',
    bgColor: 'bg-amber-50',
  },
  'web-app-basic': {
    icon: Globe,
    color: 'text-indigo-500',
    bgColor: 'bg-indigo-50',
  },
  'python': {
    icon: SiPython,
    color: 'text-[#4584b6]',
    bgColor: 'bg-[#ffde57]/20',
  },
  'git': {
    icon: SiGit,
    color: 'text-gray-700',
    bgColor: 'bg-gray-50',
  },
  'linux': {
    icon: SiLinux,
    color: 'text-yellow-600',
    bgColor: 'bg-yellow-100',
  },
  'database': {
    icon: Database,
    color: 'text-green-500',
    bgColor: 'bg-green-50',
  },
  // デフォルトアイコン（スラッグが一致しない場合）
  'default': {
    icon: Code,
    color: 'text-blue-500',
    bgColor: 'bg-blue-50',
  },
};

// 汎用的なマッピング（部分一致でも対応）
const genericCategoryMaps: Array<{ pattern: RegExp; config: CategoryIconConfig }> = [
  {
    pattern: /html|css|markup/i,
    config: categoryIconMap['html-css'],
  },
  {
    pattern: /ruby(?!.*rails)/i,
    config: categoryIconMap['ruby'],
  },
  {
    pattern: /rails|ror/i,
    config: categoryIconMap['ruby-rails'],
  },
  {
    pattern: /javascript|js|node/i,
    config: categoryIconMap['javascript'],
  },
  {
    pattern: /python|py/i,
    config: categoryIconMap['python'],
  },
  {
    pattern: /git|github|version/i,
    config: categoryIconMap['git'],
  },
  {
    pattern: /linux|terminal|command|shell/i,
    config: categoryIconMap['linux'],
  },
  {
    pattern: /database|sql|db/i,
    config: categoryIconMap['database'],
  },
  {
    pattern: /web.*app|webapp/i,
    config: categoryIconMap['web-app-basic'],
  },
];

/**
 * カテゴリーに対応するアイコン設定を取得
 */
export function getCategoryIcon(category: Category): CategoryIconConfig {
  // 1. 完全一致でのマッピング
  if (categoryIconMap[category.slug]) {
    return categoryIconMap[category.slug];
  }

  // 2. 部分一致でのマッピング
  for (const { pattern, config } of genericCategoryMaps) {
    if (pattern.test(category.slug) || pattern.test(category.name)) {
      return config;
    }
  }

  // 3. デフォルトアイコン
  return categoryIconMap['default'];
}

/**
 * カテゴリーリストを表示用の設定と組み合わせ
 */
export interface CategoryWithIcon extends Category {
  iconConfig: CategoryIconConfig;
}

export function enrichCategoriesWithIcons(categories: Category[]): CategoryWithIcon[] {
  return categories.map(category => ({
    ...category,
    iconConfig: getCategoryIcon(category),
  }));
}
