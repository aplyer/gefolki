%     « Copyright (c) 2016, Elise Koeniguer, Aurélien Plyer (Onera) » 
%     This file is part of GeFolki.
% 
%     GeFolki is free software: you can redistribute it and/or modify
%     it under the terms of the GNU General Public License as published by
%     the Free Software Foundation, either version 3 of the License, or
%     (at your option) any later version.
% 
%     GeFolki is distributed in the hope that it will be useful,
%     but WITHOUT ANY WARRANTY; without even the implied warranty of
%     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%     GNU General Public License for more details.
% 
%     You should have received a copy of the GNU General Public License
%     along with GeFolki in the file copying.txt.  
%     If not, see <http://www.gnu.org/licenses/gpl.txt>.
%
% ------------------------------------------------------------------------
%
%     GeFolki est un logiciel libre ; vous pouvez le redistribuer ou le
%     modifier suivant les termes de la GNU General Public License telle
%     que publiée par la Free Software Foundation ; soit la version 3 de la
%     licence, soit (à votre gré) toute version ultérieure.
% 
%     GeFolki est distribué dans l'espoir qu'il sera utile, mais SANS
%     AUCUNE GARANTIE ; sans même la garantie tacite de QUALITÉ MARCHANDE
%     ou d'ADÉQUATION à UN BUT PARTICULIER. Consultez la GNU General Public
%     License pour plus de détails.
% 
%     Vous devez avoir reçu une copie de la GNU General Public License en
%     même temps que Gefolki dans le fichier copying.txt ; si ce n'est pas
%     le cas, consultez % <http://www.gnu.org/licenses/gpl.txt


function res = rank(I, rad)

if(rad > 0)
    order = 1;
else
    order = -1;
end
rad = abs(rad);

res = zeros(size(I));
[nrow ncol] = size(I);
for i = 1:rad
  for j = 0:rad
    tmp = [[I(i+1:end,j+1:end) zeros(nrow-i,j)]; zeros(i,ncol)];
    if order == 1
        idx = (tmp > I);
    else
	idx = (tmp < I);
    end
    res(idx) = res(idx) + 1;
    tmp = [zeros(i,ncol);[zeros(nrow-i,j) I(1:end-i,1:end-j)]];
    if order == 1
        idx = (tmp > I);
    else
	idx = (tmp < I);
    end
    res(idx) = res(idx) + 1;
  end
end
for i = 0:rad
  for j = 1:rad
    tmp = [zeros(i,ncol);[I(1:end-i,1+j:end) zeros(nrow-i,j)]];
    if order == 1
        idx = (tmp > I);
    else
	idx = (tmp < I);
    end
    res(idx) = res(idx) + 1;
    tmp = [[zeros(nrow-i,j) I(i+1:end,1:end-j)]; zeros(i,ncol)];
    if order == 1
        idx = (tmp > I);
    else
	idx = (tmp < I);
    end
    res(idx) = res(idx) + 1;
  end
end


