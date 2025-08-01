"""
Algorithmic implementations of the 6 novel agent-specific metrics for AgentCodeEval

These metrics evaluate software development agent capabilities beyond traditional code quality.
"""

import ast
import re
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set
import difflib


class AgentMetricsCalculator:
    """Calculates the 6 novel agent-specific metrics using code analysis"""
    
    def __init__(self):
        self.architectural_patterns = {
            'mvc': ['model', 'view', 'controller', 'models', 'views', 'controllers'],
            'repository': ['repository', 'repo', 'dao', 'data_access'],
            'factory': ['factory', 'builder', 'create'],
            'observer': ['observer', 'listener', 'subscriber', 'event'],
            'strategy': ['strategy', 'algorithm', 'policy'],
            'adapter': ['adapter', 'wrapper', 'bridge']
        }

    def calculate_architectural_coherence_score(self, scenario: Dict[str, Any], 
                                             solution_code: Dict[str, str]) -> float:
        """
        ACS: Architectural Coherence Score
        Measures consistency with existing architectural patterns and design principles
        """
        
        context_files = scenario.get('context_files', [])
        task_category = scenario.get('task_category', '')
        
        # 1. Pattern consistency analysis (40%)
        pattern_score = self._analyze_pattern_consistency(solution_code, context_files)
        
        # 2. File organization coherence (30%)
        organization_score = self._analyze_file_organization(solution_code)
        
        # 3. Naming convention consistency (20%)
        naming_score = self._analyze_naming_consistency(solution_code)
        
        # 4. Import/dependency structure (10%)
        dependency_score = self._analyze_dependency_structure(solution_code)
        
        acs_score = (
            pattern_score * 0.4 +
            organization_score * 0.3 +
            naming_score * 0.2 +
            dependency_score * 0.1
        )
        
        return min(max(acs_score, 0.0), 1.0)

    def calculate_dependency_traversal_accuracy(self, scenario: Dict[str, Any], 
                                              solution_code: Dict[str, str]) -> float:
        """
        DTA: Dependency Traversal Accuracy
        Measures how accurately the agent navigates complex dependency relationships
        """
        
        # 1. Import resolution accuracy (40%)
        import_score = self._analyze_import_accuracy(solution_code)
        
        # 2. Cross-file reference validity (35%)
        reference_score = self._analyze_cross_file_references(solution_code)
        
        # 3. Dependency order correctness (25%)
        order_score = self._analyze_dependency_order(solution_code)
        
        dta_score = (
            import_score * 0.4 +
            reference_score * 0.35 +
            order_score * 0.25
        )
        
        return min(max(dta_score, 0.0), 1.0)

    def calculate_multi_session_memory_retention(self, scenario: Dict[str, Any], 
                                               solution_code: Dict[str, str]) -> float:
        """
        MMR: Multi-Session Memory Retention
        Measures context persistence and consistency across development sessions
        """
        
        task_category = scenario.get('task_category', '')
        
        # Only applicable for multi-session tasks
        if task_category != 'multi_session_development':
            return self._calculate_context_consistency(scenario, solution_code)
        
        # 1. Variable/function name consistency (40%)
        naming_consistency = self._analyze_naming_consistency_across_sessions(solution_code)
        
        # 2. Approach consistency (35%)
        approach_consistency = self._analyze_approach_consistency(solution_code)
        
        # 3. State management continuity (25%)
        state_consistency = self._analyze_state_management(solution_code)
        
        mmr_score = (
            naming_consistency * 0.4 +
            approach_consistency * 0.35 +
            state_consistency * 0.25
        )
        
        return min(max(mmr_score, 0.0), 1.0)

    def calculate_cross_file_reasoning_depth(self, scenario: Dict[str, Any], 
                                           solution_code: Dict[str, str]) -> float:
        """
        CFRD: Cross-File Reasoning Depth
        Measures understanding of multi-file relationships and coordination
        """
        
        # 1. Interface usage correctness (35%)
        interface_score = self._analyze_interface_usage(solution_code)
        
        # 2. Shared state coordination (30%)
        shared_state_score = self._analyze_shared_state_coordination(solution_code)
        
        # 3. Cross-file modification coordination (25%)
        modification_score = self._analyze_modification_coordination(solution_code, scenario)
        
        # 4. Data flow understanding (10%)
        dataflow_score = self._analyze_data_flow_understanding(solution_code)
        
        cfrd_score = (
            interface_score * 0.35 +
            shared_state_score * 0.30 +
            modification_score * 0.25 +
            dataflow_score * 0.10
        )
        
        return min(max(cfrd_score, 0.0), 1.0)

    def calculate_incremental_development_capability(self, scenario: Dict[str, Any], 
                                                   solution_code: Dict[str, str]) -> float:
        """
        IDC: Incremental Development Capability
        Measures ability to build incrementally on existing work
        """
        
        # 1. Backward compatibility preservation (40%)
        compatibility_score = self._analyze_backward_compatibility(solution_code, scenario)
        
        # 2. Code reuse efficiency (30%)
        reuse_score = self._analyze_code_reuse(solution_code, scenario)
        
        # 3. Extension pattern usage (20%)
        extension_score = self._analyze_extension_patterns(solution_code)
        
        # 4. Minimal disruption principle (10%)
        disruption_score = self._analyze_minimal_disruption(solution_code, scenario)
        
        idc_score = (
            compatibility_score * 0.4 +
            reuse_score * 0.3 +
            extension_score * 0.2 +
            disruption_score * 0.1
        )
        
        return min(max(idc_score, 0.0), 1.0)

    def calculate_information_coverage_utilization(self, scenario: Dict[str, Any], 
                                                 solution_code: Dict[str, str]) -> float:
        """
        ICU: Information Coverage Utilization
        Measures how effectively the agent uses available context information
        """
        
        context_files = scenario.get('context_files', [])
        task_prompt = scenario.get('task_prompt', '')
        
        # 1. Context file usage efficiency (40%)
        context_usage_score = self._analyze_context_usage(solution_code, context_files)
        
        # 2. Requirement coverage completeness (35%)
        requirement_score = self._analyze_requirement_coverage(solution_code, task_prompt)
        
        # 3. Information extraction accuracy (25%)
        extraction_score = self._analyze_information_extraction(solution_code, scenario)
        
        icu_score = (
            context_usage_score * 0.4 +
            requirement_score * 0.35 +
            extraction_score * 0.25
        )
        
        return min(max(icu_score, 0.0), 1.0)

    # Helper methods for detailed analysis

    def _analyze_pattern_consistency(self, solution_code: Dict[str, str], context_files: List[str]) -> float:
        """Analyze consistency with architectural patterns"""
        
        pattern_scores = []
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            # Check for architectural pattern indicators
            for pattern, keywords in self.architectural_patterns.items():
                pattern_matches = sum(1 for keyword in keywords if keyword in code_lower)
                if pattern_matches > 0:
                    # Bonus for consistent pattern usage
                    file_score += min(pattern_matches / len(keywords), 0.3)
            
            # Check for proper separation of concerns
            if self._has_clear_separation_of_concerns(code):
                file_score += 0.3
                
            # Check for consistent function/class organization
            if self._has_consistent_organization(code):
                file_score += 0.2
                
            pattern_scores.append(min(file_score, 1.0))
        
        return sum(pattern_scores) / len(pattern_scores) if pattern_scores else 0.0

    def _analyze_file_organization(self, solution_code: Dict[str, str]) -> float:
        """Analyze logical file organization"""
        
        organization_scores = []
        
        for filename, code in solution_code.items():
            score = 0.0
            
            # Check import organization (imports at top)
            if self._has_proper_import_organization(code):
                score += 0.3
                
            # Check function/class ordering
            if self._has_logical_ordering(code):
                score += 0.3
                
            # Check for proper spacing and structure
            if self._has_consistent_spacing(code):
                score += 0.2
                
            # Check for meaningful file structure
            if self._has_meaningful_structure(code):
                score += 0.2
                
            organization_scores.append(score)
        
        return sum(organization_scores) / len(organization_scores) if organization_scores else 0.0

    def _analyze_naming_consistency(self, solution_code: Dict[str, str]) -> float:
        """Analyze naming convention consistency"""
        
        naming_patterns = defaultdict(int)
        total_names = 0
        
        for filename, code in solution_code.items():
            # Extract function and variable names using regex
            function_names = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
            variable_names = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code)
            
            all_names = function_names + variable_names
            total_names += len(all_names)
            
            for name in all_names:
                # Determine naming pattern
                if '_' in name and name.islower():
                    naming_patterns['snake_case'] += 1
                elif name[0].islower() and any(c.isupper() for c in name[1:]):
                    naming_patterns['camelCase'] += 1
                elif name[0].isupper():
                    naming_patterns['PascalCase'] += 1
                else:
                    naming_patterns['other'] += 1
        
        if total_names == 0:
            return 0.5
            
        # Calculate consistency score based on dominant pattern
        max_pattern_count = max(naming_patterns.values()) if naming_patterns else 0
        consistency_score = max_pattern_count / total_names
        
        return min(consistency_score * 1.2, 1.0)  # Slight bonus for high consistency

    def _analyze_dependency_structure(self, solution_code: Dict[str, str]) -> float:
        """Analyze import and dependency structure"""
        
        dependency_scores = []
        
        for filename, code in solution_code.items():
            score = 0.0
            
            # Check for proper import statements
            import_lines = [line.strip() for line in code.split('\n') if line.strip().startswith(('import ', 'from '))]
            
            if import_lines:
                # Check import organization
                if self._are_imports_organized(import_lines):
                    score += 0.4
                    
                # Check for unused imports (basic check)
                if not self._has_unused_imports(code, import_lines):
                    score += 0.3
                    
                # Check for proper relative vs absolute imports
                if self._has_proper_import_style(import_lines):
                    score += 0.3
            
            dependency_scores.append(score)
        
        return sum(dependency_scores) / len(dependency_scores) if dependency_scores else 0.0

    def _analyze_import_accuracy(self, solution_code: Dict[str, str]) -> float:
        """Analyze accuracy of import statements"""
        
        import_scores = []
        
        for filename, code in solution_code.items():
            score = 0.0
            
            import_lines = [line.strip() for line in code.split('\n') if line.strip().startswith(('import ', 'from '))]
            
            if import_lines:
                # Check for valid import syntax
                valid_imports = sum(1 for imp in import_lines if self._is_valid_import_syntax(imp))
                score += (valid_imports / len(import_lines)) * 0.6
                
                # Check for reasonable import choices
                reasonable_imports = sum(1 for imp in import_lines if self._is_reasonable_import(imp))
                score += (reasonable_imports / len(import_lines)) * 0.4
            
            import_scores.append(score)
        
        return sum(import_scores) / len(import_scores) if import_scores else 0.0

    def _analyze_cross_file_references(self, solution_code: Dict[str, str]) -> float:
        """Analyze validity of cross-file references"""
        
        # Extract all function/class definitions
        definitions = {}
        for filename, code in solution_code.items():
            functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
            classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
            definitions[filename] = functions + classes
        
        reference_scores = []
        
        for filename, code in solution_code.items():
            score = 0.0
            
            # Find function/method calls
            calls = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
            
            if calls:
                # Check how many calls reference defined functions
                valid_references = 0
                for call in calls:
                    # Check if it's defined in any file
                    if any(call in file_definitions for file_definitions in definitions.values()):
                        valid_references += 1
                    # Or if it's a built-in/standard library function
                    elif self._is_builtin_function(call):
                        valid_references += 1
                
                score = valid_references / len(calls) if calls else 0.0
            
            reference_scores.append(score)
        
        return sum(reference_scores) / len(reference_scores) if reference_scores else 0.0

    def _analyze_dependency_order(self, solution_code: Dict[str, str]) -> float:
        """Analyze logical ordering of dependencies"""
        
        order_scores = []
        
        for filename, code in solution_code.items():
            lines = code.split('\n')
            import_section_end = 0
            
            # Find end of import section
            for i, line in enumerate(lines):
                if line.strip().startswith(('import ', 'from ')):
                    import_section_end = i
                elif line.strip() and not line.strip().startswith('#'):
                    break
            
            # Check if imports are at the top
            imports_at_top = import_section_end < min(10, len(lines) // 4)
            
            order_scores.append(1.0 if imports_at_top else 0.5)
        
        return sum(order_scores) / len(order_scores) if order_scores else 0.0

    # Additional helper methods (simplified implementations)
    
    def _has_clear_separation_of_concerns(self, code: str) -> bool:
        """Check if code has clear separation of concerns"""
        # Simple heuristic: check for multiple classes or clear function grouping
        class_count = len(re.findall(r'class\s+\w+', code))
        function_count = len(re.findall(r'def\s+\w+', code))
        return class_count > 0 or function_count > 2

    def _has_consistent_organization(self, code: str) -> bool:
        """Check for consistent code organization"""
        lines = code.split('\n')
        # Simple check: consistent indentation
        indented_lines = [line for line in lines if line.startswith('    ') or line.startswith('\t')]
        return len(indented_lines) > len(lines) * 0.3

    def _has_proper_import_organization(self, code: str) -> bool:
        """Check if imports are properly organized"""
        import_lines = [line.strip() for line in code.split('\n') if line.strip().startswith(('import ', 'from '))]
        if not import_lines:
            return True
        
        # Check if imports are grouped (stdlib, third-party, local)
        return len(import_lines) <= 10  # Simple heuristic

    def _has_logical_ordering(self, code: str) -> bool:
        """Check for logical ordering of functions/classes"""
        # Simple heuristic: classes before functions
        class_positions = [i for i, line in enumerate(code.split('\n')) if line.strip().startswith('class ')]
        function_positions = [i for i, line in enumerate(code.split('\n')) if line.strip().startswith('def ')]
        
        if not class_positions or not function_positions:
            return True
        
        return max(class_positions) < min(function_positions)

    def _has_consistent_spacing(self, code: str) -> bool:
        """Check for consistent spacing"""
        lines = code.split('\n')
        # Simple check: not too many blank lines
        blank_lines = sum(1 for line in lines if not line.strip())
        return blank_lines < len(lines) * 0.3

    def _has_meaningful_structure(self, code: str) -> bool:
        """Check for meaningful code structure"""
        # Simple heuristic: has docstrings or comments
        has_docstrings = '"""' in code or "'''" in code
        has_comments = '#' in code
        return has_docstrings or has_comments

    def _are_imports_organized(self, import_lines: List[str]) -> bool:
        """Check if imports are well organized"""
        # Simple heuristic: standard library imports before others
        stdlib_imports = ['os', 'sys', 'json', 'time', 'datetime', 'collections', 're']
        
        stdlib_found = False
        thirdparty_found = False
        
        for line in import_lines:
            is_stdlib = any(lib in line for lib in stdlib_imports)
            if is_stdlib:
                if thirdparty_found:
                    return False  # stdlib after third-party
                stdlib_found = True
            else:
                thirdparty_found = True
        
        return True

    def _has_unused_imports(self, code: str, import_lines: List[str]) -> bool:
        """Simple check for unused imports"""
        # Extract imported names
        imported_names = []
        for line in import_lines:
            if line.startswith('import '):
                name = line.split()[1].split('.')[0]
                imported_names.append(name)
            elif line.startswith('from '):
                parts = line.split()
                if 'import' in parts:
                    idx = parts.index('import')
                    names = ' '.join(parts[idx+1:]).split(',')
                    imported_names.extend([name.strip() for name in names])
        
        # Check if names are used in code
        for name in imported_names:
            if name not in code:
                return True
        
        return False

    def _has_proper_import_style(self, import_lines: List[str]) -> bool:
        """Check for proper import style"""
        # Prefer absolute imports, avoid wildcard imports
        for line in import_lines:
            if '*' in line:
                return False
        return True

    def _is_valid_import_syntax(self, import_line: str) -> bool:
        """Check if import has valid syntax"""
        try:
            ast.parse(import_line)
            return True
        except SyntaxError:
            return False

    def _is_reasonable_import(self, import_line: str) -> bool:
        """Check if import is reasonable"""
        # Simple heuristics for reasonable imports
        suspicious_patterns = ['__', 'sys.exit', 'eval', 'exec']
        return not any(pattern in import_line for pattern in suspicious_patterns)

    def _is_builtin_function(self, func_name: str) -> bool:
        """Check if function is a built-in"""
        builtins = ['print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 
                   'range', 'enumerate', 'zip', 'map', 'filter', 'sum', 'max', 'min', 
                   'open', 'abs', 'round', 'sorted', 'reversed']
        return func_name in builtins

    # Real implementations replacing placeholders
    def _calculate_context_consistency(self, scenario: Dict[str, Any], solution_code: Dict[str, str]) -> float:
        """Calculate how well solution maintains context consistency"""
        
        task_prompt = scenario.get('task_prompt', '')
        context_files = scenario.get('context_files', [])
        
        # 1. Context file reference consistency (40%)
        context_ref_score = self._analyze_context_usage(solution_code, context_files)
        
        # 2. Task requirement alignment (35%)
        requirement_score = self._analyze_requirement_coverage(solution_code, task_prompt)
        
        # 3. Terminology consistency (25%)
        terminology_score = self._analyze_terminology_consistency(solution_code, scenario)
        
        return (
            context_ref_score * 0.4 +
            requirement_score * 0.35 +
            terminology_score * 0.25
        )

    def _analyze_naming_consistency_across_sessions(self, solution_code: Dict[str, str]) -> float:
        """Analyze naming consistency across multiple development sessions"""
        
        all_identifiers = {}
        total_inconsistencies = 0
        total_comparisons = 0
        
        # Extract all identifiers (functions, variables, types)
        for filename, code in solution_code.items():
            identifiers = self._extract_identifiers(code)
            all_identifiers[filename] = identifiers
        
        # Compare naming patterns across files
        file_names = list(all_identifiers.keys())
        for i in range(len(file_names)):
            for j in range(i + 1, len(file_names)):
                file1_ids = all_identifiers[file_names[i]]
                file2_ids = all_identifiers[file_names[j]]
                
                # Check for similar concepts with different naming
                inconsistencies = self._find_naming_inconsistencies(file1_ids, file2_ids)
                total_inconsistencies += inconsistencies
                total_comparisons += len(file1_ids) + len(file2_ids)
        
        if total_comparisons == 0:
            return 0.5
        
        consistency_ratio = 1.0 - (total_inconsistencies / total_comparisons)
        return max(consistency_ratio, 0.0)

    def _analyze_approach_consistency(self, solution_code: Dict[str, str]) -> float:
        """Analyze consistency of programming approach across files"""
        
        approach_indicators = {
            'error_handling': ['try', 'catch', 'error', 'exception', 'if err'],
            'data_structures': ['map', 'slice', 'array', 'list', 'dict'],
            'patterns': ['interface', 'struct', 'class', 'factory', 'builder'],
            'style': ['func', 'function', 'method', 'procedure']
        }
        
        file_approaches = {}
        
        # Analyze approach in each file
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_approach = {}
            
            for category, indicators in approach_indicators.items():
                usage_count = sum(1 for indicator in indicators if indicator in code_lower)
                file_approach[category] = usage_count
                
            file_approaches[filename] = file_approach
        
        # Calculate consistency across files
        if len(file_approaches) < 2:
            return 0.8  # Single file, assume consistent
        
        consistency_scores = []
        categories = list(approach_indicators.keys())
        
        for category in categories:
            category_values = [approaches.get(category, 0) for approaches in file_approaches.values()]
            category_variance = self._calculate_variance(category_values)
            category_consistency = 1.0 / (1.0 + category_variance)  # Higher variance = lower consistency
            consistency_scores.append(category_consistency)
        
        return sum(consistency_scores) / len(consistency_scores)

    def _analyze_state_management(self, solution_code: Dict[str, str]) -> float:
        """Analyze quality of state management patterns"""
        
        state_indicators = {
            'immutability': ['const', 'readonly', 'immutable', 'copy'],
            'shared_state': ['global', 'static', 'shared', 'singleton'],
            'state_isolation': ['private', 'encapsulated', 'local'],
            'state_validation': ['validate', 'check', 'verify', 'assert']
        }
        
        total_score = 0.0
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            # Check for good state management patterns
            for pattern, indicators in state_indicators.items():
                pattern_usage = sum(1 for indicator in indicators if indicator in code_lower)
                if pattern_usage > 0:
                    if pattern == 'immutability' or pattern == 'state_isolation':
                        file_score += 0.3  # Bonus for good patterns
                    elif pattern == 'shared_state':
                        file_score -= 0.1  # Penalty for shared state
                    else:
                        file_score += 0.1
            
            # Check for state mutation patterns
            mutation_patterns = ['=', '++', '--', '+=', '-=']
            mutation_count = sum(code.count(pattern) for pattern in mutation_patterns)
            
            # Penalize excessive mutations
            if mutation_count > 10:
                file_score -= 0.2
            
            total_score += max(file_score, 0.0)
        
        return min(total_score / len(solution_code), 1.0)

    def _analyze_interface_usage(self, solution_code: Dict[str, str]) -> float:
        """Analyze proper interface design and usage"""
        
        interface_patterns = {
            'interface_definition': ['interface', 'protocol', 'abstract'],
            'dependency_injection': ['inject', 'provide', 'wire', 'bind'],
            'abstraction': ['implement', 'extend', 'inherit', 'override'],
            'contracts': ['requires', 'ensures', 'contract', 'guarantee']
        }
        
        total_score = 0.0
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            # Check for interface patterns
            for pattern, indicators in interface_patterns.items():
                pattern_usage = sum(1 for indicator in indicators if indicator in code_lower)
                if pattern_usage > 0:
                    file_score += 0.25
            
            # Check for proper interface naming (ends with -er, -able, or Interface)
            interface_names = re.findall(r'interface\s+([A-Za-z]+)', code)
            proper_interface_names = sum(1 for name in interface_names 
                                       if name.endswith(('er', 'able', 'Interface')))
            
            if interface_names:
                file_score += (proper_interface_names / len(interface_names)) * 0.2
            
            total_score += min(file_score, 1.0)
        
        return total_score / len(solution_code)

    def _analyze_shared_state_coordination(self, solution_code: Dict[str, str]) -> float:
        """Analyze coordination of shared state across files"""
        
        coordination_patterns = {
            'synchronization': ['mutex', 'lock', 'sync', 'atomic', 'synchronized'],
            'messaging': ['channel', 'queue', 'event', 'message', 'signal'],
            'coordination': ['wait', 'notify', 'coordinate', 'barrier'],
            'isolation': ['goroutine', 'thread', 'process', 'worker']
        }
        
        total_coordination_score = 0.0
        shared_state_detected = False
        
        # First, detect if shared state exists
        for filename, code in solution_code.items():
            code_lower = code.lower()
            if any(pattern in code_lower for pattern in ['global', 'static', 'shared']):
                shared_state_detected = True
                break
        
        if not shared_state_detected:
            return 0.8  # No shared state, good isolation
        
        # Analyze coordination mechanisms
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            for pattern, indicators in coordination_patterns.items():
                pattern_usage = sum(1 for indicator in indicators if indicator in code_lower)
                if pattern_usage > 0:
                    file_score += 0.25
            
            total_coordination_score += min(file_score, 1.0)
        
        return total_coordination_score / len(solution_code)

    def _analyze_modification_coordination(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze coordination of modifications across multiple files"""
        
        modification_patterns = {
            'transaction': ['transaction', 'commit', 'rollback', 'begin'],
            'validation': ['validate', 'check', 'verify', 'ensure'],
            'consistency': ['consistent', 'atomic', 'ACID', 'integrity'],
            'error_recovery': ['recover', 'retry', 'fallback', 'compensate']
        }
        
        # Check if this is a modification-heavy task
        task_category = scenario.get('task_category', '')
        task_prompt = scenario.get('task_prompt', '').lower()
        
        is_modification_task = any(word in task_prompt for word in 
                                 ['update', 'modify', 'change', 'edit', 'alter', 'refactor'])
        
        if not is_modification_task:
            return 0.6  # Neutral score for non-modification tasks
        
        total_score = 0.0
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            for pattern, indicators in modification_patterns.items():
                pattern_usage = sum(1 for indicator in indicators if indicator in code_lower)
                if pattern_usage > 0:
                    file_score += 0.25
            
            # Check for proper change tracking
            if 'version' in code_lower or 'changelog' in code_lower:
                file_score += 0.1
            
            total_score += min(file_score, 1.0)
        
        return total_score / len(solution_code)

    def _analyze_data_flow_understanding(self, solution_code: Dict[str, str]) -> float:
        """Analyze understanding of data flow patterns"""
        
        data_flow_patterns = {
            'input_validation': ['validate', 'sanitize', 'check', 'verify'],
            'data_transformation': ['transform', 'convert', 'map', 'filter'],
            'output_formatting': ['format', 'serialize', 'marshal', 'encode'],
            'error_propagation': ['error', 'exception', 'fail', 'panic']
        }
        
        total_score = 0.0
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            # Check for data flow patterns
            for pattern, indicators in data_flow_patterns.items():
                pattern_usage = sum(1 for indicator in indicators if indicator in code_lower)
                if pattern_usage > 0:
                    file_score += 0.2
            
            # Check for proper data flow structure (input -> process -> output)
            has_input = any(word in code_lower for word in ['input', 'request', 'param'])
            has_process = any(word in code_lower for word in ['process', 'handle', 'execute'])
            has_output = any(word in code_lower for word in ['output', 'response', 'return'])
            
            flow_completeness = sum([has_input, has_process, has_output]) / 3.0
            file_score += flow_completeness * 0.4
            
            total_score += min(file_score, 1.0)
        
        return total_score / len(solution_code)

    def _analyze_backward_compatibility(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze maintenance of backward compatibility"""
        
        compatibility_indicators = {
            'versioning': ['version', 'v1', 'v2', 'deprecated', 'legacy'],
            'adaptation': ['adapter', 'wrapper', 'bridge', 'facade'],
            'migration': ['migrate', 'upgrade', 'transition', 'convert'],
            'deprecation': ['deprecated', 'obsolete', 'remove', 'replace']
        }
        
        task_prompt = scenario.get('task_prompt', '').lower()
        is_compatibility_relevant = any(word in task_prompt for word in 
                                      ['update', 'upgrade', 'migrate', 'compatibility', 'legacy'])
        
        if not is_compatibility_relevant:
            return 0.7  # Neutral score when compatibility isn't relevant
        
        total_score = 0.0
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            for pattern, indicators in compatibility_indicators.items():
                pattern_usage = sum(1 for indicator in indicators if indicator in code_lower)
                if pattern_usage > 0:
                    if pattern == 'deprecation':
                        file_score += 0.1  # Small bonus for handling deprecation
                    else:
                        file_score += 0.3
            
            # Check for proper API preservation
            if 'api' in code_lower and 'breaking' not in code_lower:
                file_score += 0.2
            
            total_score += min(file_score, 1.0)
        
        return total_score / len(solution_code)

    def _analyze_code_reuse(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze effective code reuse patterns"""
        
        reuse_patterns = {
            'functions': ['func', 'function', 'def', 'method'],
            'modules': ['import', 'include', 'require', 'use'],
            'inheritance': ['extends', 'inherit', 'implement', 'interface'],
            'composition': ['compose', 'mixin', 'trait', 'delegate']
        }
        
        # Detect code duplication
        code_blocks = []
        for filename, code in solution_code.items():
            lines = [line.strip() for line in code.split('\n') if line.strip()]
            code_blocks.extend(lines)
        
        # Simple duplication detection
        unique_lines = set(code_blocks)
        duplication_ratio = 1.0 - (len(unique_lines) / len(code_blocks)) if code_blocks else 0.0
        
        reuse_score = 0.0
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            # Check for reuse patterns
            for pattern, indicators in reuse_patterns.items():
                pattern_usage = sum(1 for indicator in indicators if indicator in code_lower)
                if pattern_usage > 0:
                    file_score += 0.25
            
            reuse_score += min(file_score, 1.0)
        
        # Combine reuse patterns with duplication analysis
        pattern_score = reuse_score / len(solution_code)
        duplication_penalty = duplication_ratio * 0.5  # Penalize duplication
        
        return max(pattern_score - duplication_penalty, 0.0)

    def _analyze_extension_patterns(self, solution_code: Dict[str, str]) -> float:
        """Analyze extensibility and extension patterns"""
        
        extensibility_patterns = {
            'interfaces': ['interface', 'protocol', 'contract'],
            'plugins': ['plugin', 'extension', 'addon', 'module'],
            'hooks': ['hook', 'callback', 'listener', 'event'],
            'factories': ['factory', 'builder', 'creator', 'generator']
        }
        
        total_score = 0.0
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            # Check for extensibility patterns
            for pattern, indicators in extensibility_patterns.items():
                pattern_usage = sum(1 for indicator in indicators if indicator in code_lower)
                if pattern_usage > 0:
                    file_score += 0.25
            
            # Check for configuration support
            if any(word in code_lower for word in ['config', 'setting', 'option', 'parameter']):
                file_score += 0.15
            
            # Check for modular structure
            if any(word in code_lower for word in ['module', 'component', 'service', 'package']):
                file_score += 0.1
            
            total_score += min(file_score, 1.0)
        
        return total_score / len(solution_code)

    def _analyze_minimal_disruption(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze minimal disruption to existing codebase"""
        
        task_prompt = scenario.get('task_prompt', '').lower()
        context_files = scenario.get('context_files', [])
        
        # Check if this is a modification/integration task
        is_modification_task = any(word in task_prompt for word in 
                                 ['add', 'integrate', 'extend', 'enhance', 'modify'])
        
        if not is_modification_task:
            return 0.7  # Neutral score for new implementations
        
        disruption_indicators = {
            'breaking_changes': ['breaking', 'remove', 'delete', 'replace'],
            'non_breaking': ['add', 'extend', 'enhance', 'backward', 'compatible'],
            'isolation': ['separate', 'isolate', 'encapsulate', 'module'],
            'integration': ['integrate', 'connect', 'link', 'bridge']
        }
        
        total_score = 0.0
        
        for filename, code in solution_code.items():
            code_lower = code.lower()
            file_score = 0.0
            
            # Penalize breaking changes
            breaking_count = sum(1 for indicator in disruption_indicators['breaking_changes'] 
                               if indicator in code_lower)
            file_score -= breaking_count * 0.2
            
            # Reward non-breaking approaches
            non_breaking_count = sum(1 for indicator in disruption_indicators['non_breaking'] 
                                   if indicator in code_lower)
            file_score += non_breaking_count * 0.3
            
            # Reward isolation
            isolation_count = sum(1 for indicator in disruption_indicators['isolation'] 
                                if indicator in code_lower)
            file_score += isolation_count * 0.2
            
            total_score += max(file_score, 0.0)
        
        return min(total_score / len(solution_code), 1.0)

    # Helper methods for the new implementations
    def _extract_identifiers(self, code: str) -> List[str]:
        """Extract function and variable identifiers from code"""
        # Go-specific patterns
        go_functions = re.findall(r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
        go_variables = re.findall(r'var\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
        go_types = re.findall(r'type\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
        
        # General patterns
        general_functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
        general_variables = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:?=', code)
        
        return go_functions + go_variables + go_types + general_functions + general_variables

    def _find_naming_inconsistencies(self, identifiers1: List[str], identifiers2: List[str]) -> int:
        """Find naming inconsistencies between two sets of identifiers"""
        inconsistencies = 0
        
        # Simple heuristic: check for similar concepts with different naming styles
        for id1 in identifiers1:
            for id2 in identifiers2:
                # Check if they might represent similar concepts
                if self._are_similar_concepts(id1, id2):
                    # Check if naming styles are different
                    style1 = self._get_naming_style(id1)
                    style2 = self._get_naming_style(id2)
                    if style1 != style2:
                        inconsistencies += 1
        
        return inconsistencies

    def _are_similar_concepts(self, name1: str, name2: str) -> bool:
        """Check if two names might represent similar concepts"""
        # Simple similarity check based on common roots
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        # Check for common prefixes/suffixes
        common_roots = ['get', 'set', 'create', 'update', 'delete', 'handle', 'process']
        
        for root in common_roots:
            if root in name1_lower and root in name2_lower:
                return True
        
        return False

    def _get_naming_style(self, name: str) -> str:
        """Determine the naming style of an identifier"""
        if '_' in name and name.islower():
            return 'snake_case'
        elif name[0].islower() and any(c.isupper() for c in name[1:]):
            return 'camelCase'
        elif name[0].isupper():
            return 'PascalCase'
        else:
            return 'other'

    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance

    def _analyze_terminology_consistency(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze consistency of domain terminology usage"""
        
        # Extract domain terms from task prompt
        task_prompt = scenario.get('task_prompt', '')
        domain_terms = re.findall(r'\b[A-Z][a-z]+\b', task_prompt)
        
        if not domain_terms:
            return 0.6  # Neutral score if no clear domain terms
        
        total_code = ' '.join(solution_code.values())
        term_usage_consistency = 0.0
        
        for term in set(domain_terms):
            # Check if term is used consistently across solution
            term_variants = [term, term.lower(), term.upper()]
            usage_count = sum(total_code.count(variant) for variant in term_variants)
            
            if usage_count > 0:
                term_usage_consistency += 1.0 / len(set(domain_terms))
        
        return min(term_usage_consistency, 1.0)

    # Real implementations for remaining methods
    def _analyze_architectural_extraction(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze information extraction for architectural understanding tasks"""
        
        description = scenario.get('description', '').lower()
        task_prompt = scenario.get('task_prompt', '').lower()
        combined_text = description + ' ' + task_prompt
        total_code = ' '.join(solution_code.values()).lower()
        
        # 1. Architecture pattern recognition (40%)
        architecture_patterns = [
            'middleware', 'handler', 'controller', 'service', 'repository', 'model',
            'mvc', 'rest', 'api', 'router', 'endpoint', 'interface', 'struct',
            'package', 'module', 'component', 'layer', 'tier'
        ]
        
        pattern_extraction_score = 0.0
        patterns_mentioned = [p for p in architecture_patterns if p in combined_text]
        patterns_implemented = [p for p in patterns_mentioned if p in total_code]
        
        if patterns_mentioned:
            pattern_extraction_score = len(patterns_implemented) / len(patterns_mentioned)
        
        # 2. Structural element extraction (35%)
        structural_keywords = ['function', 'method', 'class', 'struct', 'interface', 'package']
        structural_score = 0.0
        
        for keyword in structural_keywords:
            if keyword in combined_text:
                # Check if solution implements this structural element
                if keyword == 'function' and 'func ' in total_code:
                    structural_score += 1
                elif keyword == 'struct' and 'type ' in total_code and 'struct' in total_code:
                    structural_score += 1
                elif keyword == 'interface' and 'interface' in total_code:
                    structural_score += 1
                elif keyword == 'package' and 'package ' in total_code:
                    structural_score += 1
        
        structural_score = min(structural_score / 4.0, 1.0)
        
        # 3. Dependency relationship extraction (25%)
        dependency_keywords = ['import', 'dependency', 'require', 'use', 'call', 'invoke']
        dependency_score = 0.0
        
        deps_mentioned = [d for d in dependency_keywords if d in combined_text]
        deps_implemented = [d for d in deps_mentioned if d in total_code or 'import' in total_code]
        
        if deps_mentioned:
            dependency_score = len(deps_implemented) / len(deps_mentioned)
        
        return (
            pattern_extraction_score * 0.4 +
            structural_score * 0.35 +
            dependency_score * 0.25
        )

    def _analyze_feature_extraction(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze information extraction for feature implementation tasks"""
        
        description = scenario.get('description', '').lower()
        task_prompt = scenario.get('task_prompt', '').lower()
        combined_text = description + ' ' + task_prompt
        total_code = ' '.join(solution_code.values()).lower()
        
        # 1. Business logic extraction (45%)
        business_keywords = [
            'user', 'customer', 'order', 'product', 'payment', 'account', 'profile',
            'create', 'update', 'delete', 'get', 'list', 'search', 'filter',
            'validate', 'process', 'calculate', 'generate', 'send', 'receive'
        ]
        
        business_extraction_score = 0.0
        business_mentioned = [k for k in business_keywords if k in combined_text]
        business_implemented = [k for k in business_mentioned if k in total_code]
        
        if business_mentioned:
            business_extraction_score = len(business_implemented) / len(business_mentioned)
        
        # 2. Data flow extraction (30%)
        data_flow_keywords = [
            'input', 'output', 'request', 'response', 'data', 'parameter',
            'return', 'result', 'json', 'xml', 'struct', 'map', 'array', 'slice'
        ]
        
        data_flow_score = 0.0
        data_mentioned = [k for k in data_flow_keywords if k in combined_text]
        data_implemented = [k for k in data_mentioned if k in total_code]
        
        if data_mentioned:
            data_flow_score = len(data_implemented) / len(data_mentioned)
        
        # 3. Error handling extraction (25%)
        error_keywords = ['error', 'exception', 'fail', 'invalid', 'check', 'validate']
        error_score = 0.0
        
        errors_mentioned = [e for e in error_keywords if e in combined_text]
        if errors_mentioned:
            # Check for Go error handling patterns
            has_error_handling = (
                'if err != nil' in total_code or
                'error' in total_code or
                'return' in total_code and 'err' in total_code
            )
            error_score = 1.0 if has_error_handling else 0.5
        
        return (
            business_extraction_score * 0.45 +
            data_flow_score * 0.30 +
            error_score * 0.25
        )

    def _analyze_general_extraction(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze information extraction for general tasks"""
        
        description = scenario.get('description', '').lower()
        task_prompt = scenario.get('task_prompt', '').lower()
        combined_text = description + ' ' + task_prompt
        total_code = ' '.join(solution_code.values()).lower()
        
        # 1. Key concept extraction (40%)
        # Extract nouns and important keywords from scenario
        import re
        
        # Simple noun extraction (words that are capitalized or technical terms)
        concept_patterns = re.findall(r'\b[A-Z][a-z]+\b|\b(?:func|struct|interface|package|import)\b', 
                                    description + ' ' + task_prompt)
        concept_score = 0.0
        
        if concept_patterns:
            concepts_in_code = [c for c in concept_patterns if c.lower() in total_code]
            concept_score = len(concepts_in_code) / len(concept_patterns)
        
        # 2. Action extraction (35%)
        action_keywords = [
            'implement', 'create', 'build', 'add', 'update', 'modify', 'delete',
            'handle', 'process', 'manage', 'execute', 'run', 'start', 'stop'
        ]
        
        action_score = 0.0
        actions_mentioned = [a for a in action_keywords if a in combined_text]
        
        if actions_mentioned:
            # Check if solution has function definitions (actions implemented)
            func_count = total_code.count('func ')
            action_score = min(func_count / len(actions_mentioned), 1.0)
        
        # 3. Technical requirement extraction (25%)
        tech_keywords = [
            'http', 'json', 'api', 'rest', 'endpoint', 'server', 'client',
            'database', 'sql', 'query', 'connection', 'session', 'cookie'
        ]
        
        tech_score = 0.0
        tech_mentioned = [t for t in tech_keywords if t in combined_text]
        tech_implemented = [t for t in tech_mentioned if t in total_code]
        
        if tech_mentioned:
            tech_score = len(tech_implemented) / len(tech_mentioned)
        
        return (
            concept_score * 0.4 +
            action_score * 0.35 +
            tech_score * 0.25
        )

    def _analyze_context_usage(self, solution_code: Dict[str, str], context_files: List[str]) -> float:
        """Analyze how well the solution uses provided context"""
        context_usage_score = 0.0
        
        if not context_files:
            return 0.5
        
        # Check if solution references context file patterns
        for filename, code in solution_code.items():
            for context_file in context_files:
                context_name = Path(context_file).stem
                if context_name.lower() in code.lower():
                    context_usage_score += 1.0 / len(context_files)
        
        return min(context_usage_score, 1.0)

    def _analyze_requirement_coverage(self, solution_code: Dict[str, str], task_prompt: str) -> float:
        """Analyze how well solution covers task requirements"""
        if not task_prompt:
            return 0.5
        
        # Extract key requirements from task prompt
        requirement_keywords = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]*)*\b', task_prompt)
        requirement_keywords.extend(['implement', 'create', 'add', 'update', 'fix', 'analyze'])
        
        coverage_score = 0.0
        total_code = ' '.join(solution_code.values()).lower()
        
        for keyword in set(requirement_keywords):
            if keyword.lower() in total_code:
                coverage_score += 1.0 / len(set(requirement_keywords))
        
        return min(coverage_score, 1.0)

    def _analyze_information_extraction(self, solution_code: Dict[str, str], scenario: Dict[str, Any]) -> float:
        """Analyze quality of information extraction from scenario"""
        task_category = scenario.get('task_category', '')
        
        # Different extraction strategies based on task category
        if task_category == 'architectural_understanding':
            return self._analyze_architectural_extraction(solution_code, scenario)
        elif task_category == 'feature_implementation':
            return self._analyze_feature_extraction(solution_code, scenario)
        else:
            return self._analyze_general_extraction(solution_code, scenario) 