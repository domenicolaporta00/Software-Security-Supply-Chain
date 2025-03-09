{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww28600\viewh14940\viewkind0
\deftab720
\pard\pardeftab720\sa240\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
// SPDX-License-Identifier: MIT\
pragma solidity ^0.8.0;\
\
/**\
 * @title AgroToken\
 * @dev Gestisce le transazioni token e le azioni compensative nella filiera agroalimentare.\
 * Le aziende possono creare transazioni per inviare o richiedere token, e\
 * il contratto registra queste operazioni con uno stato iniziale di Pending.\
 * Inoltre, il proprietario del contratto (o eventuali indirizzi autorizzati) pu\'f2 aggiornare\
 * lo stato delle transazioni e applicare azioni compensative per modificare i bilanci token.\
 */\
contract AgroToken \{\
    // Stato del token\
    string public name = "AgroToken";\
    string public symbol = "AGT";\
    uint8 public decimals = 18;\
    uint256 public totalSupply;\
\
    // Mapping dei bilanci degli indirizzi\
    mapping(address => uint256) public balanceOf;\
\
    // Enum per il tipo e lo stato delle transazioni token\
    enum TransactionType \{ Invia, Richiedi \}\
    enum TransactionStatus \{ Pending, Completed, Rejected \}\
\
    // Struct per registrare le transazioni token\
    struct TokenTransaction \{\
        uint256 id;\
        address aziendaDa;\
        address aziendaA;\
        TransactionType tipo;\
        uint256 valore;\
        string motivo;\
        TransactionStatus status;\
        uint256 timestamp;\
    \}\
    uint256 private transactionCounter;\
    mapping(uint256 => TokenTransaction) public transactions;\
\
    // Struct per registrare le azioni compensative\
    struct CompensationAction \{\
        uint256 id;\
        address company;\
        int256 amount; // Valore positivo per aggiunte, negativo per deduzioni\
        string description;\
        uint256 timestamp;\
    \}\
    uint256 private actionCounter;\
    mapping(uint256 => CompensationAction) public compensationActions;\
\
    // Proprietario del contratto\
    address public owner;\
\
    // Eventi\
    event Transfer(address indexed from, address indexed to, uint256 value);\
    event TransactionCreated(\
        uint256 indexed id,\
        address indexed aziendaDa,\
        address indexed aziendaA,\
        TransactionType tipo,\
        uint256 valore,\
        string motivo\
    );\
    event TransactionStatusUpdated(uint256 indexed id, TransactionStatus newStatus);\
    event CompensationApplied(\
        uint256 indexed id,\
        address indexed company,\
        int256 amount,\
        string description,\
        uint256 timestamp\
    );\
\
    // Modifier per limitare l'accesso alle funzioni critiche al solo proprietario\
    modifier onlyOwner() \{\
        require(msg.sender == owner, "Accesso negato: solo il proprietario puo' eseguire questa funzione");\
        _;\
    \}\
\
    /**\
     * @dev Costruttore: imposta il proprietario e l'offerta iniziale.\
     * @param _initialSupply Offerta iniziale di token.\
     */\
    constructor(uint256 _initialSupply) \{\
        owner = msg.sender;\
        totalSupply = _initialSupply * 10 ** uint256(decimals);\
        balanceOf[owner] = totalSupply;\
        transactionCounter = 0;\
        actionCounter = 0;\
    \}\
\
    /**\
     * @dev Funzione di trasferimento base.\
     * @param _to Indirizzo destinatario.\
     * @param _value Quantit\'e0 di token da trasferire.\
     */\
    function transfer(address _to, uint256 _value) public returns (bool success) \{\
        require(_to != address(0), "Destinatario non valido");\
        require(balanceOf[msg.sender] >= _value, "Saldo insufficiente");\
        balanceOf[msg.sender] -= _value;\
        balanceOf[_to] += _value;\
        emit Transfer(msg.sender, _to, _value);\
        return true;\
    \}\
\
    /**\
     * @dev Crea una nuova transazione token.\
     * @param _aziendaA Indirizzo dell'azienda destinataria.\
     * @param _tipo Tipo di transazione (0: Invia, 1: Richiedi).\
     * @param _valore Quantit\'e0 di token.\
     * @param _motivo Descrizione della transazione.\
     * @return id della transazione creata.\
     */\
    function createTokenTransaction(\
        address _aziendaA,\
        TransactionType _tipo,\
        uint256 _valore,\
        string memory _motivo\
    ) public returns (uint256) \{\
        require(_aziendaA != address(0), "Destinatario non valido");\
        transactionCounter++;\
        transactions[transactionCounter] = TokenTransaction(\{\
            id: transactionCounter,\
            aziendaDa: msg.sender,\
            aziendaA: _aziendaA,\
            tipo: _tipo,\
            valore: _valore,\
            motivo: _motivo,\
            status: TransactionStatus.Pending,\
            timestamp: block.timestamp\
        \});\
        emit TransactionCreated(transactionCounter, msg.sender, _aziendaA, _tipo, _valore, _motivo);\
        return transactionCounter;\
    \}\
\
    /**\
     * @dev Aggiorna lo stato di una transazione token.\
     * @param _id ID della transazione.\
     * @param _newStatus Nuovo stato (Completed o Rejected).\
     * Solo il proprietario pu\'f2 aggiornare lo stato (o potresti implementare ulteriori controlli).\
     */\
    function updateTransactionStatus(uint256 _id, TransactionStatus _newStatus) public onlyOwner returns (bool) \{\
        require(transactions[_id].id != 0, "Transazione non esistente");\
        require(transactions[_id].status == TransactionStatus.Pending, "Transazione non in stato Pending");\
        transactions[_id].status = _newStatus;\
        emit TransactionStatusUpdated(_id, _newStatus);\
        return true;\
    \}\
\
    /**\
     * @dev Applica un'azione compensativa che modifica il bilancio token di un'azienda.\
     * @param _company Indirizzo dell'azienda.\
     * @param _amount Quantit\'e0 di token da aggiungere (se positiva) o dedurre (se negativa).\
     * @param _description Descrizione dell'azione compensativa.\
     */\
    function applyCompensation(\
        address _company,\
        int256 _amount,\
        string memory _description\
    ) public onlyOwner returns (bool) \{\
        require(_company != address(0), "Indirizzo azienda non valido");\
        if (_amount < 0) \{\
            // Deduzione: verificare che il saldo sia sufficiente\
            uint256 deduction = uint256(-_amount);\
            require(balanceOf[_company] >= deduction, "Saldo insufficiente per deduzione");\
            balanceOf[_company] -= deduction;\
            totalSupply -= deduction;\
        \} else \{\
            // Aggiunta\
            balanceOf[_company] += uint256(_amount);\
            totalSupply += uint256(_amount);\
        \}\
        actionCounter++;\
        compensationActions[actionCounter] = CompensationAction(\{\
            id: actionCounter,\
            company: _company,\
            amount: _amount,\
            description: _description,\
            timestamp: block.timestamp\
        \});\
        emit CompensationApplied(actionCounter, _company, _amount, _description, block.timestamp);\
        return true;\
    \}\
\}\
}