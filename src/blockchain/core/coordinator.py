import torch
from ..blockchain_code.blockchain_manager import BlockchainManager

class Coordinator:
    def __init__(self, clients, server, blockchain_manager):
        self.clients = clients
        self.server = server
        self.bm = blockchain_manager

    def run_round(self, round_num):
        print(f"\n--- Début du Round {round_num} ---")
        
        for client in self.clients:
            total_loss = 0
            correct = 0
            total = 0
            
            # On simule l'entraînement sur quelques batches
            for i, (data, labels) in enumerate(client.dataloader):
                #if i >= 10: break
                
                # 1. Forward Client
                smashed_data = client.forward(data)
                
                # 2. Forward Serveur
                output = self.server.forward(smashed_data)
                
                # 3. Backward Serveur
                smash_grad, loss_val = self.server.backward(labels)
                
                # 4. Backward Client
                client.backward(smash_grad)
                
                # Métriques
                total_loss += loss_val
                _, predicted = torch.max(output.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            accuracy = 100 * correct / total
            avg_loss = total_loss / 10
            
            # 5. Enregistrement Blockchain RÉEL sur Ganache
            print(f"🔗 Envoi à la blockchain pour Client {client.client_id}...")
            self.bm.send_training_record(
                client.address, 
                client.private_key, 
                round_num, 
                client.model.get_model_hash(), 
                accuracy, 
                avg_loss
            )
            print(f"✅ Client {client.client_id} : Acc {accuracy:.2f}% | Loss {avg_loss:.4f}")