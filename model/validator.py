"""
Input Validator - Rilevamento attacchi SQL Injection, XSS, Command Injection, Path Traversal
"""
import re

class InputValidator:
    """
    Classe per validare input utente e rilevare pattern malevoli
    """
    
    # Pattern SQL Injection
    SQL_PATTERNS = [
        r"(\bOR\b|\bAND\b)\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?",  # OR 1=1, AND 1=1
        r"UNION\s+SELECT",                                             # UNION SELECT
        r"DROP\s+(TABLE|DATABASE|SCHEMA)",                            # DROP TABLE/DATABASE
        r"INSERT\s+INTO",                                             # INSERT INTO
        r"DELETE\s+FROM",                                             # DELETE FROM
        r"UPDATE\s+\w+\s+SET",                                        # UPDATE SET
        r"--",                                                        # SQL comment
        r";\s*DROP",                                                  # ; DROP
        r"';\s*--",                                                   # '; --
        r"'\s*OR\s*'",                                               # ' OR '
        r"admin'\s*--",                                              # admin'--
        r"'\s*=\s*'",                                                # ' = '
        r"1'\s*=\s*'1",                                              # 1'='1
    ]
    
    # Pattern XSS (Cross-Site Scripting)
    XSS_PATTERNS = [
        r"<script[^>]*>",                                            # <script>
        r"</script>",                                                # </script>
        r"javascript:",                                              # javascript:
        r"on\w+\s*=",                                               # onclick=, onload=, onerror=
        r"<iframe[^>]*>",                                           # <iframe>
        r"<embed[^>]*>",                                            # <embed>
        r"<object[^>]*>",                                           # <object>
        r"<img[^>]*onerror",                                        # <img onerror=
        r"<svg[^>]*onload",                                         # <svg onload=
        r"alert\s*\(",                                              # alert(
        r"eval\s*\(",                                               # eval(
        r"document\.cookie",                                        # document.cookie
        r"window\.location",                                        # window.location
    ]
    
    # Pattern Command Injection
    COMMAND_PATTERNS = [
        r";\s*rm\s+-rf",                                            # ; rm -rf
        r";\s*cat\s+",                                              # ; cat
        r"\|\s*cat\s+",                                             # | cat
        r"&&\s*(rm|del|format)",                                    # && rm/del/format
        r"`.*`",                                                    # backticks
        r"\$\(.*\)",                                                # $(command)
        r">\s*/dev/null",                                           # > /dev/null
        r";\s*curl\s+",                                             # ; curl
        r";\s*wget\s+",                                             # ; wget
        r"\|\s*nc\s+",                                              # | nc (netcat)
        r";\s*bash",                                                # ; bash
        r";\s*sh\s+",                                               # ; sh
    ]
    
    # Pattern Path Traversal
    PATH_PATTERNS = [
        r"\.\./",                                                   # ../
        r"\.\./\.\./",                                              # ../../
        r"\.\.\\",                                                  # ..\
        r"%2e%2e%2f",                                              # URL encoded ../
        r"%2e%2e/",                                                # Mixed encoding
        r"\.\.%2f",                                                # Mixed encoding
        r"/etc/passwd",                                            # /etc/passwd
        r"/etc/shadow",                                            # /etc/shadow
        r"c:\\windows\\system32",                                  # Windows system
        r"c:/windows/system32",                                    # Windows system
    ]
    
    @staticmethod
    def validate(input_string, field_name="input"):
        """
        Valida una stringa per rilevare pattern malevoli
        
        Args:
            input_string (str): Stringa da validare
            field_name (str): Nome del campo (per logging)
        
        Returns:
            dict: {
                'is_safe': bool,
                'attack_type': str | None,
                'pattern_matched': str | None,
                'field': str
            }
        """
        if not input_string or not isinstance(input_string, str):
            return {
                'is_safe': True,
                'attack_type': None,
                'pattern_matched': None,
                'field': field_name
            }
        
        # Converti in uppercase per case-insensitive matching
        input_upper = input_string.upper()
        
        # Check SQL Injection
        for pattern in InputValidator.SQL_PATTERNS:
            if re.search(pattern, input_upper, re.IGNORECASE):
                return {
                    'is_safe': False,
                    'attack_type': 'SQL_INJECTION',
                    'pattern_matched': pattern,
                    'field': field_name,
                    'input_sample': input_string[:100]  # primi 100 caratteri
                }
        
        # Check XSS
        for pattern in InputValidator.XSS_PATTERNS:
            if re.search(pattern, input_string, re.IGNORECASE):
                return {
                    'is_safe': False,
                    'attack_type': 'XSS',
                    'pattern_matched': pattern,
                    'field': field_name,
                    'input_sample': input_string[:100]
                }
        
        # Check Command Injection
        for pattern in InputValidator.COMMAND_PATTERNS:
            if re.search(pattern, input_string, re.IGNORECASE):
                return {
                    'is_safe': False,
                    'attack_type': 'COMMAND_INJECTION',
                    'pattern_matched': pattern,
                    'field': field_name,
                    'input_sample': input_string[:100]
                }
        
        # Check Path Traversal
        for pattern in InputValidator.PATH_PATTERNS:
            if re.search(pattern, input_string, re.IGNORECASE):
                return {
                    'is_safe': False,
                    'attack_type': 'PATH_TRAVERSAL',
                    'pattern_matched': pattern,
                    'field': field_name,
                    'input_sample': input_string[:100]
                }
        
        # Nessun pattern malevolo trovato
        return {
            'is_safe': True,
            'attack_type': None,
            'pattern_matched': None,
            'field': field_name
        }
    
    @staticmethod
    def validate_multiple(fields_dict):
        """
        Valida multipli campi contemporaneamente
        
        Args:
            fields_dict (dict): {'field_name': 'value', ...}
        
        Returns:
            dict: {
                'is_safe': bool,
                'failed_validations': list
            }
        """
        failed = []
        
        for field_name, value in fields_dict.items():
            result = InputValidator.validate(value, field_name)
            if not result['is_safe']:
                failed.append(result)
        
        return {
            'is_safe': len(failed) == 0,
            'failed_validations': failed
        }
