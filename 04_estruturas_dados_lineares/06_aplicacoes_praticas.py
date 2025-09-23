"""
Módulo: Aplicações Práticas das Estruturas Lineares
Tópico: Casos de Uso Reais e Projetos Integrados
Autor: Professor Python - Lógica e Estruturas de Dados
Nível: Intermediário/Avançado

Objetivos de Aprendizado:
- Aplicar estruturas lineares em problemas reais
- Integrar múltiplas estruturas em soluções
- Implementar sistemas completos
- Analisar trade-offs de design
- Otimizar para casos específicos
- Criar APIs robustas
- Implementar padrões de design
- Resolver problemas complexos

Conceitos Abordados:
- Sistema de cache LRU
- Editor de texto com undo/redo
- Simulador de CPU com scheduling
- Sistema de mensagens
- Calculadora de expressões
- Navegador web simplificado
- Sistema de playlist
- Analisador de logs

Pré-requisitos:
- Todas as estruturas lineares
- Conceitos de OOP
- Padrões de design
- Análise de complexidade

Aplicações:
- Cache systems
- Text editors
- Operating systems
- Web browsers
- Media players
- Log analyzers
- Expression evaluators
- Message queues
"""

from typing import Any, Optional, Dict, List, Tuple, Iterator, Generic, TypeVar
from collections import deque, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import re
import time
import threading
from abc import ABC, abstractmethod
import heapq
import json

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

def introducao_aplicacoes():
    """
    Introduz as aplicações práticas das estruturas lineares.
    """
    print("=== APLICAÇÕES PRÁTICAS DAS ESTRUTURAS LINEARES ===")
    print()
    
    print("1. MAPEAMENTO PROBLEMA → ESTRUTURA:")
    print()
    print("   ┌─────────────────────────────────────────────────────────────────────────────┐")
    print("   │                        GUIA DE ESCOLHA                                      │")
    print("   ├─────────────────────────────────────────────────────────────────────────────┤")
    print("   │                                                                             │")
    print("   │  PROBLEMA                          ESTRUTURA IDEAL        JUSTIFICATIVA    │")
    print("   │  ─────────────────────────────────────────────────────────────────────────  │")
    print("   │  Cache com limite de tamanho       LRU Cache (Dict+Deque)  O(1) acesso     │")
    print("   │  Undo/Redo operations             Stack + Stack           LIFO natural     │")
    print("   │  Scheduling de processos           Priority Queue         Ordenação auto   │")
    print("   │  Buffer de mensagens               Queue/Deque            FIFO processing  │")
    print("   │  Expressões matemáticas            Stack                  Parsing natural  │")
    print("   │  Histórico de navegação            Deque                  Acesso duplo     │")
    print("   │  Playlist de música                Lista Ligada           Inserção flex    │")
    print("   │  Log analysis                      Array Dinâmico         Acesso indexado  │")
    print("   │  Sliding window                    Deque                  Extremidades O(1) │")
    print("   │  Autocomplete                      Trie + Lista           Busca eficiente  │")
    print("   │                                                                             │")
    print("   └─────────────────────────────────────────────────────────────────────────────┘")
    print()
    
    print("2. PADRÕES DE DESIGN COMUNS:")
    print()
    print("   • Observer Pattern: Lista de observadores")
    print("   • Command Pattern: Stack de comandos para undo")
    print("   • Strategy Pattern: Lista de estratégias")
    print("   • Iterator Pattern: Navegação em estruturas")
    print("   • Composite Pattern: Árvore de componentes")
    print("   • Chain of Responsibility: Lista ligada de handlers")
    print()
    
    print("3. CONSIDERAÇÕES DE PERFORMANCE:")
    print()
    print("   ┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐")
    print("   │   OPERAÇÃO      │    ARRAY    │    LISTA    │    STACK    │    DEQUE    │")
    print("   ├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤")
    print("   │ Acesso aleatório│    O(1)     │    O(n)     │     N/A     │  O(1)/O(n)  │")
    print("   │ Inserção início │    O(n)     │    O(1)     │     N/A     │    O(1)     │")
    print("   │ Inserção fim    │  O(1) amort │    O(n)     │    O(1)     │    O(1)     │")
    print("   │ Busca elemento  │    O(n)     │    O(n)     │    O(n)     │    O(n)     │")
    print("   │ Uso de memória  │   Compacto  │  Overhead   │   Compacto  │   Médio     │")
    print("   │ Cache locality  │     Boa     │    Ruim     │     Boa     │    Boa      │")
    print("   └─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘")
    print()

class LRUCache(Generic[K, V]):
    """
    Implementação de cache LRU (Least Recently Used) usando dict + deque.
    Combina O(1) para acesso e O(1) para manutenção da ordem.
    """
    
    @dataclass
    class _Node:
        """Nó interno do cache"""
        key: K
        value: V
        timestamp: float = field(default_factory=time.time)
    
    def __init__(self, capacity: int):
        """
        Inicializa cache LRU.
        
        Args:
            capacity: Capacidade máxima do cache
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self._cache: Dict[K, LRUCache._Node] = {}
        self._order: deque = deque()  # Mantém ordem de uso
        
        # Estatísticas
        self._hits = 0
        self._misses = 0
        self._evictions = 0
    
    def get(self, key: K) -> Optional[V]:
        """
        Obtém valor do cache - O(1).
        
        Args:
            key: Chave a ser buscada
            
        Returns:
            Valor associado à chave ou None se não encontrado
        """
        if key in self._cache:
            # Hit: mover para final (mais recente)
            self._order.remove(key)
            self._order.append(key)
            self._cache[key].timestamp = time.time()
            self._hits += 1
            return self._cache[key].value
        
        # Miss
        self._misses += 1
        return None
    
    def put(self, key: K, value: V) -> None:
        """
        Insere/atualiza valor no cache - O(1).
        
        Args:
            key: Chave
            value: Valor
        """
        if key in self._cache:
            # Atualizar valor existente
            self._cache[key].value = value
            self._cache[key].timestamp = time.time()
            self._order.remove(key)
            self._order.append(key)
        else:
            # Nova entrada
            if len(self._cache) >= self.capacity:
                # Evict LRU (primeiro da deque)
                lru_key = self._order.popleft()
                del self._cache[lru_key]
                self._evictions += 1
            
            # Adicionar nova entrada
            self._cache[key] = self._Node(key, value)
            self._order.append(key)
    
    def delete(self, key: K) -> bool:
        """
        Remove entrada do cache - O(1).
        
        Args:
            key: Chave a ser removida
            
        Returns:
            True se removido, False se não encontrado
        """
        if key in self._cache:
            del self._cache[key]
            self._order.remove(key)
            return True
        return False
    
    def clear(self) -> None:
        """Limpa todo o cache"""
        self._cache.clear()
        self._order.clear()
    
    def keys(self) -> List[K]:
        """Retorna chaves em ordem de uso (LRU primeiro)"""
        return list(self._order)
    
    def values(self) -> List[V]:
        """Retorna valores em ordem de uso"""
        return [self._cache[key].value for key in self._order]
    
    def items(self) -> List[Tuple[K, V]]:
        """Retorna pares chave-valor em ordem de uso"""
        return [(key, self._cache[key].value) for key in self._order]
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0
        
        return {
            'size': len(self._cache),
            'capacity': self.capacity,
            'utilization': len(self._cache) / self.capacity,
            'hits': self._hits,
            'misses': self._misses,
            'evictions': self._evictions,
            'hit_rate': hit_rate,
            'total_requests': total_requests
        }
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def __contains__(self, key: K) -> bool:
        return key in self._cache
    
    def __str__(self) -> str:
        items = [f"{k}: {self._cache[k].value}" for k in self._order]
        return f"LRUCache([{', '.join(items)}])"

class TextEditor:
    """
    Editor de texto com undo/redo usando stacks.
    Demonstra uso de múltiplas estruturas integradas.
    """
    
    class Command(ABC):
        """Comando abstrato para pattern Command"""
        
        @abstractmethod
        def execute(self) -> None:
            pass
        
        @abstractmethod
        def undo(self) -> None:
            pass
        
        @abstractmethod
        def get_description(self) -> str:
            pass
    
    class InsertCommand(Command):
        """Comando de inserção de texto"""
        
        def __init__(self, editor: 'TextEditor', position: int, text: str):
            self.editor = editor
            self.position = position
            self.text = text
        
        def execute(self) -> None:
            self.editor._content = (
                self.editor._content[:self.position] + 
                self.text + 
                self.editor._content[self.position:]
            )
            self.editor._cursor = self.position + len(self.text)
        
        def undo(self) -> None:
            self.editor._content = (
                self.editor._content[:self.position] + 
                self.editor._content[self.position + len(self.text):]
            )
            self.editor._cursor = self.position
        
        def get_description(self) -> str:
            preview = self.text[:20] + "..." if len(self.text) > 20 else self.text
            return f"Insert '{preview}' at {self.position}"
    
    class DeleteCommand(Command):
        """Comando de deleção de texto"""
        
        def __init__(self, editor: 'TextEditor', position: int, length: int):
            self.editor = editor
            self.position = position
            self.length = length
            self.deleted_text = ""
        
        def execute(self) -> None:
            self.deleted_text = self.editor._content[self.position:self.position + self.length]
            self.editor._content = (
                self.editor._content[:self.position] + 
                self.editor._content[self.position + self.length:]
            )
            self.editor._cursor = self.position
        
        def undo(self) -> None:
            self.editor._content = (
                self.editor._content[:self.position] + 
                self.deleted_text + 
                self.editor._content[self.position:]
            )
            self.editor._cursor = self.position + len(self.deleted_text)
        
        def get_description(self) -> str:
            preview = self.deleted_text[:20] + "..." if len(self.deleted_text) > 20 else self.deleted_text
            return f"Delete '{preview}' from {self.position}"
    
    def __init__(self, max_history: int = 100):
        """
        Inicializa editor de texto.
        
        Args:
            max_history: Máximo de comandos no histórico
        """
        self._content = ""
        self._cursor = 0
        self.max_history = max_history
        
        # Stacks para undo/redo
        self._undo_stack: List[TextEditor.Command] = []
        self._redo_stack: List[TextEditor.Command] = []
        
        # Estatísticas
        self._total_commands = 0
        self._total_undos = 0
        self._total_redos = 0
    
    def insert(self, text: str, position: Optional[int] = None) -> None:
        """
        Insere texto na posição especificada.
        
        Args:
            text: Texto a ser inserido
            position: Posição de inserção (cursor atual se None)
        """
        if position is None:
            position = self._cursor
        
        command = self.InsertCommand(self, position, text)
        self._execute_command(command)
    
    def delete(self, length: int, position: Optional[int] = None) -> str:
        """
        Deleta texto da posição especificada.
        
        Args:
            length: Número de caracteres a deletar
            position: Posição inicial (cursor atual se None)
            
        Returns:
            Texto deletado
        """
        if position is None:
            position = self._cursor
        
        # Ajustar length para não exceder conteúdo
        length = min(length, len(self._content) - position)
        
        if length <= 0:
            return ""
        
        deleted_text = self._content[position:position + length]
        command = self.DeleteCommand(self, position, length)
        self._execute_command(command)
        
        return deleted_text
    
    def _execute_command(self, command: Command) -> None:
        """Executa comando e adiciona ao histórico"""
        command.execute()
        
        # Adicionar ao undo stack
        self._undo_stack.append(command)
        
        # Limitar tamanho do histórico
        if len(self._undo_stack) > self.max_history:
            self._undo_stack.pop(0)
        
        # Limpar redo stack (nova ação invalida redo)
        self._redo_stack.clear()
        
        self._total_commands += 1
    
    def undo(self) -> bool:
        """
        Desfaz última operação.
        
        Returns:
            True se operação foi desfeita, False se não há o que desfazer
        """
        if not self._undo_stack:
            return False
        
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        
        self._total_undos += 1
        return True
    
    def redo(self) -> bool:
        """
        Refaz operação desfeita.
        
        Returns:
            True se operação foi refeita, False se não há o que refazer
        """
        if not self._redo_stack:
            return False
        
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        
        self._total_redos += 1
        return True
    
    def get_content(self) -> str:
        """Retorna conteúdo atual"""
        return self._content
    
    def get_cursor_position(self) -> int:
        """Retorna posição atual do cursor"""
        return self._cursor
    
    def set_cursor_position(self, position: int) -> None:
        """Define posição do cursor"""
        self._cursor = max(0, min(position, len(self._content)))
    
    def get_line_info(self) -> Tuple[int, int]:
        """
        Retorna informações da linha atual.
        
        Returns:
            Tupla (número da linha, posição na linha)
        """
        lines_before = self._content[:self._cursor].count('\n')
        last_newline = self._content.rfind('\n', 0, self._cursor)
        column = self._cursor - last_newline - 1 if last_newline != -1 else self._cursor
        
        return lines_before + 1, column + 1
    
    def get_history(self) -> List[str]:
        """Retorna histórico de comandos"""
        return [cmd.get_description() for cmd in self._undo_stack]
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do editor"""
        lines = self._content.count('\n') + 1 if self._content else 0
        words = len(self._content.split()) if self._content else 0
        chars = len(self._content)
        
        return {
            'lines': lines,
            'words': words,
            'characters': chars,
            'cursor_position': self._cursor,
            'undo_available': len(self._undo_stack),
            'redo_available': len(self._redo_stack),
            'total_commands': self._total_commands,
            'total_undos': self._total_undos,
            'total_redos': self._total_redos
        }
    
    def __str__(self) -> str:
        """Representação do editor com cursor"""
        content_with_cursor = (
            self._content[:self._cursor] + 
            '|' + 
            self._content[self._cursor:]
        )
        return f"TextEditor: '{content_with_cursor}'"

class ProcessScheduler:
    """
    Simulador de scheduler de processos usando priority queue e deque.
    Demonstra integração de estruturas para sistemas operacionais.
    """
    
    class ProcessState(Enum):
        """Estados possíveis de um processo"""
        NEW = "new"
        READY = "ready"
        RUNNING = "running"
        WAITING = "waiting"
        TERMINATED = "terminated"
    
    @dataclass
    class Process:
        """Representação de um processo"""
        pid: int
        name: str
        priority: int  # Menor valor = maior prioridade
        burst_time: int  # Tempo de CPU necessário
        arrival_time: float
        state: 'ProcessScheduler.ProcessState' = ProcessScheduler.ProcessState.NEW
        remaining_time: int = 0
        start_time: Optional[float] = None
        finish_time: Optional[float] = None
        waiting_time: float = 0
        
        def __post_init__(self):
            if self.remaining_time == 0:
                self.remaining_time = self.burst_time
        
        def __lt__(self, other):
            # Para priority queue (menor prioridade primeiro)
            return self.priority < other.priority
    
    def __init__(self, time_quantum: int = 2):
        """
        Inicializa scheduler.
        
        Args:
            time_quantum: Quantum de tempo para round-robin
        """
        self.time_quantum = time_quantum
        self.current_time = 0.0
        
        # Filas de processos
        self._ready_queue = []  # Priority queue (heap)
        self._waiting_queue = deque()  # FIFO para processos esperando I/O
        self._finished_processes: List[ProcessScheduler.Process] = []
        
        # Processo atual
        self._current_process: Optional[ProcessScheduler.Process] = None
        self._quantum_remaining = 0
        
        # Estatísticas
        self._total_processes = 0
        self._context_switches = 0
        self._cpu_utilization_time = 0.0
    
    def add_process(self, name: str, priority: int, burst_time: int) -> int:
        """
        Adiciona novo processo ao sistema.
        
        Args:
            name: Nome do processo
            priority: Prioridade (menor = mais prioritário)
            burst_time: Tempo de CPU necessário
            
        Returns:
            PID do processo criado
        """
        pid = self._total_processes + 1
        process = self.Process(
            pid=pid,
            name=name,
            priority=priority,
            burst_time=burst_time,
            arrival_time=self.current_time
        )
        
        # Adicionar à fila de prontos
        process.state = self.ProcessState.READY
        heapq.heappush(self._ready_queue, process)
        
        self._total_processes += 1
        return pid
    
    def simulate_step(self) -> Dict[str, Any]:
        """
        Simula um passo do scheduler.
        
        Returns:
            Informações sobre o estado atual
        """
        step_info = {
            'time': self.current_time,
            'current_process': None,
            'action': 'idle',
            'ready_queue_size': len(self._ready_queue),
            'waiting_queue_size': len(self._waiting_queue)
        }
        
        # Se não há processo rodando, pegar próximo da fila
        if self._current_process is None and self._ready_queue:
            self._current_process = heapq.heappop(self._ready_queue)
            self._current_process.state = self.ProcessState.RUNNING
            self._quantum_remaining = self.time_quantum
            
            if self._current_process.start_time is None:
                self._current_process.start_time = self.current_time
            
            self._context_switches += 1
            step_info['action'] = 'context_switch'
        
        # Executar processo atual
        if self._current_process is not None:
            step_info['current_process'] = {
                'pid': self._current_process.pid,
                'name': self._current_process.name,
                'remaining_time': self._current_process.remaining_time,
                'quantum_remaining': self._quantum_remaining
            }
            
            # Executar por 1 unidade de tempo
            self._current_process.remaining_time -= 1
            self._quantum_remaining -= 1
            self._cpu_utilization_time += 1
            step_info['action'] = 'executing'
            
            # Verificar se processo terminou
            if self._current_process.remaining_time <= 0:
                self._current_process.state = self.ProcessState.TERMINATED
                self._current_process.finish_time = self.current_time + 1
                self._finished_processes.append(self._current_process)
                self._current_process = None
                step_info['action'] = 'process_finished'
            
            # Verificar se quantum acabou (preemption)
            elif self._quantum_remaining <= 0:
                self._current_process.state = self.ProcessState.READY
                heapq.heappush(self._ready_queue, self._current_process)
                self._current_process = None
                step_info['action'] = 'preemption'
        
        # Simular chegada de processos da fila de espera (I/O completed)
        if self._waiting_queue and len(self._ready_queue) < 3:  # Simular I/O completion
            process = self._waiting_queue.popleft()
            process.state = self.ProcessState.READY
            heapq.heappush(self._ready_queue, process)
            step_info['action'] = 'io_completed'
        
        self.current_time += 1
        return step_info
    
    def simulate_io_request(self, duration: int = 3) -> bool:
        """
        Simula requisição de I/O do processo atual.
        
        Args:
            duration: Duração da operação de I/O
            
        Returns:
            True se I/O foi iniciado, False se não há processo rodando
        """
        if self._current_process is None:
            return False
        
        # Mover processo para fila de espera
        self._current_process.state = self.ProcessState.WAITING
        self._waiting_queue.append(self._current_process)
        self._current_process = None
        
        return True
    
    def get_system_state(self) -> Dict[str, Any]:
        """Retorna estado completo do sistema"""
        # Calcular estatísticas dos processos terminados
        if self._finished_processes:
            avg_turnaround = sum(
                p.finish_time - p.arrival_time 
                for p in self._finished_processes
            ) / len(self._finished_processes)
            
            avg_waiting = sum(
                (p.start_time - p.arrival_time) + 
                (p.finish_time - p.start_time - p.burst_time)
                for p in self._finished_processes
            ) / len(self._finished_processes)
        else:
            avg_turnaround = 0
            avg_waiting = 0
        
        cpu_utilization = (
            self._cpu_utilization_time / self.current_time 
            if self.current_time > 0 else 0
        )
        
        return {
            'current_time': self.current_time,
            'current_process': self._current_process.name if self._current_process else None,
            'ready_queue': [p.name for p in self._ready_queue],
            'waiting_queue': [p.name for p in self._waiting_queue],
            'finished_processes': len(self._finished_processes),
            'total_processes': self._total_processes,
            'context_switches': self._context_switches,
            'cpu_utilization': cpu_utilization,
            'avg_turnaround_time': avg_turnaround,
            'avg_waiting_time': avg_waiting
        }

class MessageQueue:
    """
    Sistema de mensagens usando deque com prioridades.
    Demonstra uso de deque para buffering e processamento assíncrono.
    """
    
    class Priority(Enum):
        """Prioridades de mensagem"""
        LOW = 1
        NORMAL = 2
        HIGH = 3
        CRITICAL = 4
    
    @dataclass
    class Message:
        """Representação de uma mensagem"""
        id: str
        content: str
        priority: 'MessageQueue.Priority'
        timestamp: datetime
        sender: str
        recipient: str
        processed: bool = False
        retry_count: int = 0
        max_retries: int = 3
        
        def __lt__(self, other):
            # Para ordenação por prioridade (maior prioridade primeiro)
            return self.priority.value > other.priority.value
    
    def __init__(self, max_size: int = 1000):
        """
        Inicializa sistema de mensagens.
        
        Args:
            max_size: Tamanho máximo da fila
        """
        self.max_size = max_size
        
        # Filas por prioridade
        self._critical_queue = deque()
        self._high_queue = deque()
        self._normal_queue = deque()
        self._low_queue = deque()
        
        # Fila de retry
        self._retry_queue = deque()
        
        # Mensagens processadas (para auditoria)
        self._processed_messages: List[MessageQueue.Message] = []
        
        # Estatísticas
        self._total_sent = 0
        self._total_processed = 0
        self._total_failed = 0
        self._total_retries = 0
        
        # Thread safety
        self._lock = threading.Lock()
    
    def send_message(self, content: str, sender: str, recipient: str, 
                    priority: Priority = Priority.NORMAL) -> str:
        """
        Envia mensagem para a fila.
        
        Args:
            content: Conteúdo da mensagem
            sender: Remetente
            recipient: Destinatário
            priority: Prioridade da mensagem
            
        Returns:
            ID da mensagem
        """
        with self._lock:
            # Verificar se fila está cheia
            total_messages = (
                len(self._critical_queue) + len(self._high_queue) + 
                len(self._normal_queue) + len(self._low_queue)
            )
            
            if total_messages >= self.max_size:
                raise RuntimeError("Message queue is full")
            
            # Criar mensagem
            message_id = f"msg_{self._total_sent + 1}_{int(time.time())}"
            message = self.Message(
                id=message_id,
                content=content,
                priority=priority,
                timestamp=datetime.now(),
                sender=sender,
                recipient=recipient
            )
            
            # Adicionar à fila apropriada
            if priority == self.Priority.CRITICAL:
                self._critical_queue.append(message)
            elif priority == self.Priority.HIGH:
                self._high_queue.append(message)
            elif priority == self.Priority.NORMAL:
                self._normal_queue.append(message)
            else:  # LOW
                self._low_queue.append(message)
            
            self._total_sent += 1
            return message_id
    
    def receive_message(self) -> Optional[Message]:
        """
        Recebe próxima mensagem da fila (por prioridade).
        
        Returns:
            Próxima mensagem ou None se fila estiver vazia
        """
        with self._lock:
            # Verificar retry queue primeiro
            if self._retry_queue:
                return self._retry_queue.popleft()
            
            # Processar por prioridade
            if self._critical_queue:
                return self._critical_queue.popleft()
            elif self._high_queue:
                return self._high_queue.popleft()
            elif self._normal_queue:
                return self._normal_queue.popleft()
            elif self._low_queue:
                return self._low_queue.popleft()
            
            return None
    
    def process_message(self, message: Message, success: bool = True) -> None:
        """
        Marca mensagem como processada ou agenda retry.
        
        Args:
            message: Mensagem a ser processada
            success: Se processamento foi bem-sucedido
        """
        with self._lock:
            if success:
                message.processed = True
                self._processed_messages.append(message)
                self._total_processed += 1
            else:
                # Tentar novamente se não excedeu limite
                if message.retry_count < message.max_retries:
                    message.retry_count += 1
                    self._retry_queue.append(message)
                    self._total_retries += 1
                else:
                    # Falha definitiva
                    message.processed = False
                    self._processed_messages.append(message)
                    self._total_failed += 1
    
    def get_queue_sizes(self) -> Dict[str, int]:
        """Retorna tamanhos das filas"""
        with self._lock:
            return {
                'critical': len(self._critical_queue),
                'high': len(self._high_queue),
                'normal': len(self._normal_queue),
                'low': len(self._low_queue),
                'retry': len(self._retry_queue),
                'total': (
                    len(self._critical_queue) + len(self._high_queue) + 
                    len(self._normal_queue) + len(self._low_queue) + 
                    len(self._retry_queue)
                )
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema"""
        with self._lock:
            queue_sizes = self.get_queue_sizes()
            
            return {
                'total_sent': self._total_sent,
                'total_processed': self._total_processed,
                'total_failed': self._total_failed,
                'total_retries': self._total_retries,
                'success_rate': (
                    self._total_processed / self._total_sent 
                    if self._total_sent > 0 else 0
                ),
                'queue_sizes': queue_sizes,
                'queue_utilization': queue_sizes['total'] / self.max_size
            }
    
    def get_messages_by_recipient(self, recipient: str) -> List[Message]:
        """Retorna mensagens processadas para um destinatário"""
        with self._lock:
            return [
                msg for msg in self._processed_messages 
                if msg.recipient == recipient
            ]

def demonstrar_aplicacoes():
    """
    Demonstra as aplicações práticas implementadas.
    """
    print("=== DEMONSTRAÇÃO DAS APLICAÇÕES ===")
    print()
    
    print("1. CACHE LRU:")
    print()
    
    # Demonstração do cache LRU
    cache = LRUCache[str, str](capacity=3)
    
    print("   Operações no cache:")
    cache.put("user1", "Alice")
    print(f"   put('user1', 'Alice'): {cache}")
    
    cache.put("user2", "Bob")
    print(f"   put('user2', 'Bob'): {cache}")
    
    cache.put("user3", "Charlie")
    print(f"   put('user3', 'Charlie'): {cache}")
    
    print(f"   get('user1'): {cache.get('user1')} → {cache}")
    
    cache.put("user4", "David")  # Evict user2 (LRU)
    print(f"   put('user4', 'David'): {cache}")
    
    print(f"   get('user2'): {cache.get('user2')} (cache miss)")
    
    print(f"\n   Stats: {cache.get_stats()}")
    print()
    
    print("2. EDITOR DE TEXTO:")
    print()
    
    # Demonstração do editor
    editor = TextEditor(max_history=5)
    
    print("   Operações no editor:")
    editor.insert("Hello")
    print(f"   insert('Hello'): {editor}")
    
    editor.insert(" World")
    print(f"   insert(' World'): {editor}")
    
    editor.insert("!", 5)  # Inserir no meio
    print(f"   insert('!', 5): {editor}")
    
    deleted = editor.delete(6)  # Deletar " World"
    print(f"   delete(6): '{deleted}' → {editor}")
    
    print(f"\n   Histórico: {editor.get_history()}")
    
    print("\n   Undo/Redo:")
    editor.undo()
    print(f"   undo(): {editor}")
    
    editor.undo()
    print(f"   undo(): {editor}")
    
    editor.redo()
    print(f"   redo(): {editor}")
    
    print(f"\n   Stats: {editor.get_stats()}")
    print()
    
    print("3. SCHEDULER DE PROCESSOS:")
    print()
    
    # Demonstração do scheduler
    scheduler = ProcessScheduler(time_quantum=3)
    
    print("   Adicionando processos:")
    scheduler.add_process("Process A", priority=2, burst_time=5)
    scheduler.add_process("Process B", priority=1, burst_time=3)
    scheduler.add_process("Process C", priority=3, burst_time=4)
    
    print("   Simulação (primeiros 10 passos):")
    for i in range(10):
        step = scheduler.simulate_step()
        current = step['current_process']
        if current:
            print(f"   Tempo {step['time']:2}: {step['action']:15} - {current['name']} (restante: {current['remaining_time']})")
        else:
            print(f"   Tempo {step['time']:2}: {step['action']:15}")
        
        # Simular I/O request ocasionalmente
        if i == 4 and current:
            scheduler.simulate_io_request()
            print(f"   Tempo {step['time']:2}: I/O request      - {current['name']}")
    
    print(f"\n   Estado do sistema: {scheduler.get_system_state()}")
    print()
    
    print("4. SISTEMA DE MENSAGENS:")
    print()
    
    # Demonstração do sistema de mensagens
    msg_queue = MessageQueue(max_size=10)
    
    print("   Enviando mensagens:")
    msg_queue.send_message("Sistema iniciado", "system", "admin", MessageQueue.Priority.HIGH)
    msg_queue.send_message("Backup concluído", "backup", "admin", MessageQueue.Priority.NORMAL)
    msg_queue.send_message("ERRO CRÍTICO!", "database", "admin", MessageQueue.Priority.CRITICAL)
    msg_queue.send_message("Log diário", "logger", "admin", MessageQueue.Priority.LOW)
    
    print(f"   Tamanhos das filas: {msg_queue.get_queue_sizes()}")
    
    print("\n   Processando mensagens (por prioridade):")
    for i in range(4):
        message = msg_queue.receive_message()
        if message:
            print(f"   {i+1}. [{message.priority.name}] {message.sender} → {message.recipient}: {message.content}")
            # Simular falha ocasional
            success = i != 1  # Falha na segunda mensagem
            msg_queue.process_message(message, success)
            if not success:
                print(f"      ↳ Falha no processamento, agendado para retry")
    
    print(f"\n   Stats: {msg_queue.get_stats()}")
    
    # Processar retry
    retry_msg = msg_queue.receive_message()
    if retry_msg:
        print(f"\n   Processando retry: {retry_msg.content} (tentativa {retry_msg.retry_count})")
        msg_queue.process_message(retry_msg, True)
    
    print(f"   Stats finais: {msg_queue.get_stats()}")
    print()

def casos_uso_avancados():
    """
    Apresenta casos de uso mais avançados e padrões de integração.
    """
    print("=== CASOS DE USO AVANÇADOS ===")
    print()
    
    print("1. INTEGRAÇÃO DE MÚLTIPLAS ESTRUTURAS:")
    print()
    print("   Sistema de Recomendação:")
    print("   ┌─────────────────────────────────────────────────────────────────┐")
    print("   │  Cache LRU ←→ Priority Queue ←→ Deque (sliding window)          │")
    print("   │       ↓              ↓                    ↓                     │")
    print("   │  Usuários        Recomendações        Histórico                 │")
    print("   │  recentes        por score            de interações             │")
    print("   └─────────────────────────────────────────────────────────────────┘")
    print()
    
    print("2. PADRÕES DE OTIMIZAÇÃO:")
    print()
    print("   a) Lazy Loading com Cache:")
    print("      • Cache LRU para dados frequentes")
    print("      • Lista ligada para dados raramente acessados")
    print("      • Deque para buffer de pré-carregamento")
    print()
    
    print("   b) Batch Processing:")
    print("      • Queue para acumular operações")
    print("      • Array dinâmico para processamento em lote")
    print("      • Stack para rollback em caso de erro")
    print()
    
    print("   c) Event Sourcing:")
    print("      • Lista ligada para stream de eventos")
    print("      • Stack para snapshots")
    print("      • Deque para replay window")
    print()
    
    print("3. CONSIDERAÇÕES DE THREAD SAFETY:")
    print()
    print("   ┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("   │   ESTRUTURA     │   THREAD SAFE   │   SINCRONIZAÇÃO │   ALTERNATIVA   │")
    print("   ├─────────────────┼─────────────────┼─────────────────┼─────────────────┤")
    print("   │ Lista Python    │       NÃO       │      Lock       │ queue.Queue     │")
    print("   │ collections.deque│      SIM*       │    Atômica      │ queue.deque     │")
    print("   │ heapq           │       NÃO       │      Lock       │ queue.Priority  │")
    print("   │ dict            │       NÃO       │      Lock       │ threading.local │")
    print("   │ Custom classes  │    DEPENDE      │   Implementar   │ concurrent.*    │")
    print("   └─────────────────┴─────────────────┴─────────────────┴─────────────────┘")
    print("   * Operações append/popleft são thread-safe")
    print()
    
    print("4. MÉTRICAS E MONITORAMENTO:")
    print()
    print("   Métricas importantes para estruturas lineares:")
    print("   • Throughput (operações/segundo)")
    print("   • Latência (tempo de resposta)")
    print("   • Utilização de memória")
    print("   • Taxa de cache hit/miss")
    print("   • Tamanho médio das filas")
    print("   • Tempo de vida dos elementos")
    print("   • Distribuição de acessos")
    print()
    
    print("5. ANTI-PADRÕES COMUNS:")
    print()
    print("   ❌ Usar lista para operações frequentes no início")
    print("   ❌ Cache sem limite de tamanho")
    print("   ❌ Não considerar thread safety em ambiente concorrente")
    print("   ❌ Escolher estrutura baseada apenas na familiaridade")
    print("   ❌ Não medir performance em cenários reais")
    print("   ❌ Implementar do zero quando existe solução nativa")
    print("   ❌ Não documentar invariantes e pré-condições")
    print()
    
    print("6. CHECKLIST DE DESIGN:")
    print()
    print("   ✅ Analisar padrões de acesso (sequencial, aleatório, extremidades)")
    print("   ✅ Considerar frequência de operações (leitura vs escrita)")
    print("   ✅ Avaliar restrições de memória")
    print("   ✅ Definir requisitos de performance")
    print("   ✅ Considerar concorrência e thread safety")
    print("   ✅ Planejar estratégia de teste")
    print("   ✅ Implementar métricas e logging")
    print("   ✅ Documentar decisões de design")
    print()

if __name__ == "__main__":
    print("MÓDULO 4.6 - APLICAÇÕES PRÁTICAS DAS ESTRUTURAS LINEARES")
    print("=" * 60)
    print()
    
    # Executando todas as seções
    introducao_aplicacoes()
    print("\n" + "="*60 + "\n")
    
    demonstrar_aplicacoes()
    print("\n" + "="*60 + "\n")
    
    casos_uso_avancados()
    print("\n" + "="*60 + "\n")
    
    print("🎓 MÓDULO 4.6 CONCLUÍDO!")
    print("\nTópicos aprendidos:")
    print("✅ Cache LRU com dict + deque")
    print("✅ Editor de texto com undo/redo")
    print("✅ Scheduler de processos com priority queue")
    print("✅ Sistema de mensagens com múltiplas filas")
    print("✅ Integração de estruturas lineares")
    print("✅ Padrões de design com estruturas")
    print("✅ Considerações de thread safety")
    print("✅ Métricas e monitoramento")
    print("✅ Anti-padrões e boas práticas")
    print("✅ Checklist de design")
    print()
    print("🏆 MÓDULO 04 - ESTRUTURAS DE DADOS LINEARES COMPLETO!")
    print("\n➡️  Próximo: Módulo 05 - Estruturas de Dados Não-Lineares")