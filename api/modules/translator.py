from models import Rfts

class Translator:

	@staticmethod
	def filter_descricao(stage: str, defects):
		defects.pop('erro_id')

		match(stage):
			case "burnin":
				return defects["burnin_defect"]
			case "potencia":
				return ' ; '.join(defects.keys())
			case "pre_tests":
				return ' ; '.join([v for v in defects.values() if v])

	@staticmethod
	def mount_rft(rft: Rfts):

		rft_data = {
			"controladora_id": rft.serialNumber,
			"operador_id": int(rft.operadorID),
			"horario": rft.sent_in.isoformat(),
			"erro_id": int(rft.defect['erro_id']),
			"descricao": Translator.filter_descricao(rft.stage, rft.defect)
		}

		return rft_data
	
	@staticmethod
	def mount_manutencao(rft: Rfts):

		manutencao_data = {
			"operador_id": int(rft.operadorID),
			"rft_id": int(rft.rft_id),
			"solucao_id": int(rft.solucao),
			"descricao": rft.actions_taken,
			"horario": rft.start_time.isoformat().split('.')[0],
			"duracao": (rft.end_time - rft.start_time).total_seconds() / 60
		}

		return manutencao_data